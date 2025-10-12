import os
import sys
import numpy as np
import numba
import argparse

def main():
    parser = argparse.ArgumentParser(

        description='''
Compute r/m ratio (and values separately) given a folder containing expected inputs.
 
Expected inputs are:
    - core_genome folder containing:
    - sample.txt: tab-delimited file with strain names in first column.
    - distances.dist: tab-delimited file with strain names in first two columns and distance in third.
    - families.txt: tab-delimited file with family name in second column.
    - concat_names.fa: FASTA file with concatenated DNA alignment of all strains.

This script uses Numba for speed.

Written by Gavin Douglas. Based on an earlier version by Louis-Marie Bobay.
        ''',

        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input_folder',
                        help='Folder containing expected inputs (see description).',
                        type=str)
    
    parser.add_argument('-p', '--prefix_path',
                        help="Optional path to add to the input folder name.",
                        required=False,
                        default='',
                        type=str)

    parser.add_argument('-o', '--outfile',
                        help='Optional output file name. If not provided, will print to "rm1.txt" in existing core_genome folder.',
                        required=False,
                        default=None,
                        type=str)

    parser.add_argument('-q', '--quiet',
                        help='Do not print verbose log information.',
                        action='store_true')

    args = parser.parse_args()

    input_folder = args.input_folder
    print(input_folder)
    if args.prefix_path:
        input_folder = os.path.join(args.prefix_path, input_folder)


    if not os.path.exists(input_folder + '/core_genome'):
        sys.exit("Error: core_genome subfolder does not exist in input folder.")

    strains = set()
    sample_file = os.path.join(input_folder, 'core_genome/sample.txt')
    if not os.path.exists(sample_file):
        sys.exit("Error: sample file does not exist.")
    with open(sample_file, 'r') as sample_fh:
        for sample_line in sample_fh:
            a = sample_line.strip('\n').split('\t')
            strains.add(a[0])
    strains_sorted = sorted(list(strains))
    strain_to_index = {strain: i for i, strain in enumerate(strains_sorted)}

    dist = np.full((len(strains), len(strains)), np.nan, dtype=np.float64)
    np.fill_diagonal(dist, 0.0)
    dist_file = os.path.join(input_folder, 'core_genome/distances.dist')
    if not os.path.exists(dist_file):
        sys.exit("Error: distance file does not exist.")
    with open(dist_file, 'r') as dist_fh:
        for dist_line in dist_fh:
            dist_line = dist_line.strip().split()
            strain1, strain2, inter_dist = dist_line[0], dist_line[1], dist_line[2]
            if strain1 not in strains or strain2 not in strains:
                sys.exit("Error: strain not in sample file.")
            dist[strain_to_index[strain1], strain_to_index[strain2]] = float(inter_dist)
            dist[strain_to_index[strain2], strain_to_index[strain1]] = float(inter_dist)

    families = []
    families_file = os.path.join(input_folder, 'core_genome/families.txt')
    if not os.path.exists(families_file):
        sys.exit("Error: families file does not exist.")
    with open(families_file, 'r') as families_fh:
        for family_line in families_fh:
            family_line = family_line.strip('\n').split('\t')
            families.append(family_line[1])

    if not args.quiet:
        print('Finished reading strain, distance, and family files.', file=sys.stderr)

    seq = {}
    alignment_file = os.path.join(input_folder, 'core_genome/concat_names.fa')
    if not os.path.exists(alignment_file):
        sys.exit("Error: alignment file does not exist.")
    with open(alignment_file, 'r') as alignment_fh:
        last_id = None
        for line in alignment_fh:
            if line[0] == '>':
                last_id = line.strip('>').strip()
                seq[last_id] = ''
            elif last_id is None:
                sys.exit("Error: invalid alignment file - needs to start with header.")
            else:
                seq[last_id] += line.strip()

    # Make sure that all strains have an alignment, and that they are all the same length.
    alignment_length = len(seq[last_id])
    for strain in strains:
        if strain not in seq:
            sys.exit("Error: strain " + strain + " does not have an alignment.")
        if len(seq[strain]) != alignment_length:
            sys.exit("Error: alignment length for strain " + strain + " does not match other strains.")

    print('Finished reading all files.', file=sys.stderr)

    base_to_i = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

    # Convert bases to 0, 1, 2, 3 and store in a numpy array.
    # Note that NaN indicated by -1.
    seq_array = np.full((len(strains), alignment_length), -1, dtype=np.int8)
    for strain_id in seq:
        strain_i = strain_to_index[strain_id]
        for i, base in enumerate(seq[strain_id]):
            if base in base_to_i:
                seq_array[strain_i, i] = base_to_i[base]

    # Remove all columns that have all the same value (i.e., no variation). Ignores NaN (indicated by -1).
    unique_states = np.array([len(np.unique(col[col >= 0])) for col in seq_array.T])
    seq_array = seq_array[:, unique_states > 1]

    if seq_array.shape[1] == 0:
        sys.exit("Error: no variation in alignment.")

    if not args.quiet:
        print('Finished creating numpy representation of alignment. Now starting main algorithm.', file=sys.stderr)

    @numba.jit(nopython=True)
    def compute_r_m_based_on_group_dists_numba(ingroup, outgroup):
        max_dist_strains_ingroup = 0.0
        min_dist_strains_w_diff = 1e9
        for i in range(ingroup.shape[0]):
            for j in range(i + 1, ingroup.shape[0]):
                current_dist = dist[ingroup[i], ingroup[j]]
                if current_dist > max_dist_strains_ingroup:
                    max_dist_strains_ingroup = current_dist

            for k in range(outgroup.shape[0]):
                outgroup_dist = dist[ingroup[i], outgroup[k]]
                if outgroup_dist < min_dist_strains_w_diff:
                    min_dist_strains_w_diff = outgroup_dist

        if max_dist_strains_ingroup > min_dist_strains_w_diff:
            return 1
        else:
            return 0

    @numba.jit(nopython=True)
    def process_bases_at_site_numba(strains_i):
        '''
        Core function to compute r/m for a a given set of strain indices.
        Note that this works on integer representations of strains and bases,
        to make it easy to use Numba.
        '''
        r = 0
        m = 0

        align_subset = seq_array[strains_i, :]

        subset_unique_states = np.array([len(np.unique(col[col >= 0])) for col in align_subset.T])
        align_subset = align_subset[:, subset_unique_states > 1]

        for i in range(align_subset.shape[1]):
            base_tallies = np.zeros(4, dtype=np.int32)
            for base_j in align_subset[:, i]:
                if base_j >= 0:
                    base_tallies[base_j] += 1
            num_muts = 0
            num_singletons = 0
            for possible_base in range(4):
                # Ignore singletons, but count as mutations.
                if base_tallies[possible_base] == 1:
                    num_singletons += 1
                elif base_tallies[possible_base] > 1:
                    num_muts += 1

            # Only count singleton as mutation if it is not the only base present.
            if num_singletons > 1 or num_muts > 0:
                m += num_singletons

            sorted_i = np.argsort(base_tallies)
            if num_muts == 2:
                minor = sorted_i[2]
                major = sorted_i[3]
                sac = strains_i[np.where(align_subset[:, i] == minor)[0]]

                # Note that this way of include "other" strains can sometimes include strains with singletons, rather than the major allele.
                # This was done to match the original implementation.
                other = strains_i[(align_subset[:, i] != minor) & (align_subset[:, i] != -1)]
                # This would be the better way of doing it in the future:
                # other = strains_i[np.where(align_subset[:, i] == major)[0]]

                if compute_r_m_based_on_group_dists_numba(sac, other) == 1:
                    r += 1
                else:
                    m += 1

            elif num_muts == 3:
                minor1, minor2, major = sorted_i[1], sorted_i[2], sorted_i[3]
                sac1 = strains_i[np.where(align_subset[:, i] == minor1)[0]]
                sac2 = strains_i[np.where(align_subset[:, i] == minor2)[0]]

                # Note that this way of include "other" strains can sometimes include strains with singletons, rather than the major allele.
                # This was done to match the original implementation.
                other = strains_i[(align_subset[:, i] != minor1) & (align_subset[:, i] != minor2) & (align_subset[:, i] != -1)]
                # This would be the better way of doing it in the future:
                # other = strains_i[np.where(align_subset[:, i] == major)[0]]

                if compute_r_m_based_on_group_dists_numba(sac1, other) == 1:
                    r += 1
                else:
                    m += 1

                if compute_r_m_based_on_group_dists_numba(sac2, other) == 1:
                    r += 1
                else:
                    m += 1

            elif num_muts == 4:
                minor1, minor2, minor3, major = sorted_i[0], sorted_i[1], sorted_i[2], sorted_i[3]
                sac1 = strains_i[np.where(align_subset[:, i] == minor1)[0]]
                sac2 = strains_i[np.where(align_subset[:, i] == minor2)[0]]
                sac3 = strains_i[np.where(align_subset[:, i] == minor3)[0]]
                other = strains_i[np.where(align_subset[:, i] == major)[0]]

                if compute_r_m_based_on_group_dists_numba(sac1, other) == 1:
                    r += 1
                else:
                    m += 1

                if compute_r_m_based_on_group_dists_numba(sac2, other) == 1:
                    r += 1
                else:
                    m += 1

                if compute_r_m_based_on_group_dists_numba(sac3, other) == 1:
                    r += 1
                else:
                    m += 1
        return r, m

    if args.outfile:
        outfile = args.outfile
    else:
        outfile = os.path.join(input_folder, 'core_genome/rm1.txt')
    with open(outfile, 'w') as out_fh:
        for family in families:
            strains = family.split(';')
            strains_i = np.array([strain_to_index[strain] for strain in strains])
            r, m = process_bases_at_site_numba(strains_i)

            try:
                r_m = float(r) / float(m)
            except ZeroDivisionError:
                r_m = 'NA'
            out_fh.write(family + '\t' + str(r) + '\t' + str(m) + '\t' + str(r_m) + '\n')


if __name__ == '__main__':
    main()


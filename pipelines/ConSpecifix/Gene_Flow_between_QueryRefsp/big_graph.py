#!/usr/bin/env python3
import sys
from pathlib import Path

# Dynamically detect project root
project_root = Path(__file__).resolve().parents[3]

# Get species from command line
sp_name = sys.argv[-1]
species = [sp_name]

for sp in species:
    try:
        big_graph_file = project_root / sp / "big_graph.R"
        with open(big_graph_file, "w") as h:

            NB, nb = 1, 0
            for sp_inner in species:
                nb += 1
                if nb == 1:
                    h.write(f"pdf('{project_root / sp_inner / 'Graph.pdf'}')\n")
                    h.write("par(mfrow=c(3,3))\n")
                h.write(f"tab = read.table('{project_root / sp_inner / 'graph.txt'}', h=T)\n")
                h.write('w=c(tab$Nb,rev(tab$Nb))\n')
                h.write('v=c(tab$Median-tab$SD,rev(tab$Median + tab$SD))\n')
                h.write(
                    f'plot(100,100,cex=0.5,cex.main=0.8,xlim=c(3,max(w)),ylim=c(0,max(v)+0.1),'
                    f'xlab=c("# Genomes"),ylab=c("h/m"),main="{sp_inner}")\n'
                )
                h.write('polygon(w,v,col="gray88",border=NA)\n')
                h.write('points(tab$Nb,tab$Median,pch=16,cex=0.3,t="b")\n')
                if nb == 9:
                    nb = 0
                    NB += 1
                    h.write("dev.off()\n\n")

            h.write("dev.off()\n\n")

    except IOError:
        pass

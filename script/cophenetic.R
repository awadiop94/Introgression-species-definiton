require('ape')
require('MASS')



files = list.files('../root1')

for (stuff in files){
toto = grep(".tree",c(stuff))
if (length(toto) == 1){


toto2 = grep("renamed",stuff)
if (length(toto2==1)){


name = paste('../root1/',stuff,sep="")
print(stuff)
tree = read.tree(name)
dist = cophenetic(tree)
output = paste('../root1/distance_',stuff,sep="")
write.matrix(dist,file=output)
}
}}

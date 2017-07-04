#################################################################
# Initialisation
#################################################################

library(igraph)
library(viridis)

rm(list = ls())
gc()

#################################################################
# Reading Datasets
#################################################################

#read colorcodes
CC <- read.csv("../data/color_coding.csv")

#read the data
SCDR <- read.csv('../R_data/evolution/R_SC_DR_evol_13.csv', header=F)
SCSR <- read.csv('../R_data/evolution/R_SC_SR_evol_13.csv', header=F)

#coerce it into a matrix in the form of an adjacency matrix
ADJ_SCDR <- as.matrix(SCDR)
ADJ_SCSR <- as.matrix(SCSR)

#################################################################
# Generating 'igraph' objects
#################################################################

G_SCDR <- graph.adjacency(ADJ_SCDR, mode="directed", weight=TRUE)
G_SCSR <- graph.adjacency(ADJ_SCSR, mode="directed", weight=TRUE)

G_SCDR <- simplify(G_SCDR, remove.multiple = F, remove.loops = T)
G_SCSR <- simplify(G_SCSR, remove.multiple = F, remove.loops = T)

#################################################################
# Accessing Graph statistics.
#################################################################

#getting graph density
D_G_SCDR <- graph.density(G_SCDR)
D_G_SCSR <-graph.density(G_SCSR)

#degree vector of individuals.
deg_SCDR <- degree(G_SCDR, mode="all")
deg_SCSR <- degree(G_SCDR, mode="all")

#edge weights
T_SCDR <- get.edge.attribute(G_SCDR, "weight")
T_SCSR <- get.edge.attribute(G_SCSR, "weight")

#################################################################
# Processing igraph objects
#################################################################

E(G_SCSR)$width <- E(G_SCSR)$weight*3.0
E(G_SCDR)$width <- E(G_SCDR)$weight*3.0

#Looking at dyads
#----------------------------------------------------------------

# "DYAD_SCSR ----------- "
# dyad.census(G_SCSR)
# "DYAD_SCDR ----------- "
# dyad.census(G_SCDR)

#Looking at triad
#----------------------------------------------------------------

# "TRIAD_SCSR ----------- "
# triad.census(G_SCSR)
# "TRIAD_SCDR ----------- "
# triad.census(G_SCDR)

#Looking at clusters
#----------------------------------------------------------------

# "CL_SCSR ----------- "
# clusters(G_SCSR)
# "CL_SCDR ----------- "
# clusters(G_SCDR)

#experimention
#----------------------------------------------------------------


"Graph density values"
graph.density(G_SCSR)
graph.density(G_SCDR)

# #################################################################
# #Visualisation
# #################################################################

# colrs <- rep(c('darkseagreen','mediumpurple3'), each=20)

# l <- layout.fruchterman.reingold(G_SCSR)
# m <- layout.fruchterman.reingold(G_SCDR)

# #Same colony Same retreat
# #----------------------------------------------------------------
# V(G_SCSR)$color <- colrs[V(G_SCSR)]
# C_SCSR <- walktrap.community(G_SCSR)
# C_SCSR
# plot(G_SCSR,
# 	vertex.size=5.5,
# 	edge.arrow.size=.45,
# 	edge.color='darkslategrey',
# 	vertex.label=NA,
# 	vertex.frame.color=NA,
# 	layout=l*3.0)

# title("SC_SR",cex.main=0.8, col.main="darkslategrey")

# plot(C_SCSR ,G_SCSR,
# 	vertex.size=5.5,
# 	edge.arrow.size=.45,
# 	edge.color='darkslategrey',
#  	vertex.label=NA,
# 	vertex.frame.color=NA,
# 	layout=l*3.0)

# title("SC_SR Community",cex.main=0.8, col.main="darkslategrey")

# #Same colony different retreat
# #----------------------------------------------------------------
# V(G_SCDR)$color <- colrs[V(G_SCDR)]
# C_SCDR <- walktrap.community(G_SCDR)
# C_SCDR

# plot(G_SCDR,
# 	vertex.size=5.5,
# 	edge.arrow.size=.45,
# 	edge.color='darkslategrey',
# 	vertex.label=NA,
# 	vertex.frame.color=NA,
# 	layout=m*3.0)

# title("SC_DR",cex.main=0.8, col.main="darkslategrey")

# plot(C_SCDR ,G_SCDR,
# 	vertex.size=5,
# 	edge.arrow.size=.5,
# 	edge.color='darkslategrey',
# 	vertex.label=NA,
# 	vertex.frame.color=NA,
# 	layout=m*3.0)

# title("SC_DR Community",cex.main=0.8, col.main="darkslategrey")


# # #################################################################
# # # Experimental
# # #################################################################

# #generate heat maps
# #----------------------------------------------------------------

# pallete <- viridis(500.0, alpha = 1, begin = 0, end = 1, option = "D")

# H_SCSR <- get.adjacency(G_SCSR, attr="weight", sparse=F)

# colnames(H_SCSR) <- CC$code
# rownames(H_SCSR) <- CC$code

# heatmap(H_SCSR, Colv = NA, Rowv = NA,
# 	col = pallete, scale="none", margins=c(10,10))

# title("SC_SR",cex.main=0.8, col.main="white")

# #----------------------------------------------------------------

# H_SCDR <- get.adjacency(G_SCDR, attr="weight", sparse=F)

# rownames(H_SCDR) <- CC$code
# colnames(H_SCDR) <- CC$code

# heatmap(H_SCDR, Colv = NA, Rowv = NA,
# 	col = pallete, scale="none", margins=c(10,10))

# title("SC_DR",cex.main=0.8, col.main="white")

# #plotting degree of individuals. [Huge problem with axes.]
# #----------------------------------------------------------------

# DD_SCSR <- degree.distribution(G_SCSR, cumulative=T, mode="all")
# DD_SCDR <- degree.distribution(G_SCDR, cumulative=T, mode="all")

# plot(DD_SCDR, pch=19, cex=1, col="orange",
# 	xlab="Degree", ylab="Cumulative Frequency", type = "b", axes=T)

# par(new=T)

# #----------------------------------------------------------------
# plot(DD_SCSR, pch=19, cex=1, col="red",
# 	xlab="", ylab="", type = "b", axes=T)

# title("Degree distribution",cex.main=0.8, col.main="black")

# legend('topright', legend=c('SC_DR', 'SC_SR'),
# 	col=c("orange", "red"), pch=19:19, cex=0.8)

# # dev.off()

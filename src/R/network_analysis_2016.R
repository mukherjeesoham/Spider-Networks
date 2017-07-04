# packages
install.packages("igraph")
library(igraph)

# set working directory to directory where TCGA_prostate_RPPA.txt was downloaded
# setwd("Desktop/3S_2014/")  (just an example)

# read matrix in
m <- read.table("TCGA_prostate_RPPA.txt", sep="\t", row.names=1, header=T)

# exploration - what does data look like ?
# how many rows and columns ?
# overall distribution of data points (columns)
# visualize

# get number of rows
dim(m) 

# boxplot of columns
boxplot(m)

# heatmap
heatmap(as.matrix(m))

# column correlation matrix
cormat <- cor(t(m))

# set diagnonal to 0 (removes self-correlation)
diag(cormat) <- 0

# EXERCISE: what does the histogram of correlations looks like ? is there a natural threshold ?

# set all correlation < 0.7 to 0
cormat[ cormat < 0.7 ] <- 0

# igraph: create graph based on adjacency matrix
graph <- graph.adjacency(cormat, weighted=TRUE, mode="lower")

# how many nodes ?
vcount(graph)

# how many edges
ecount(graph)

# display nodes (vertices)
V(graph)

# display edges
E(graph)

# igraph: plot graph
plot.igraph(graph,vertex.size=3, layout=layout.lgl, vertex.label.cex=0.5, vertex.label=NA)

# igraph: change layout
plot.igraph(graph,vertex.size=3,layout=layout.kamada.kawai, vertex.label.cex=0.5, vertex.label=NA)

# set color of node 1 to red
V(graph)[1]$color <- "red"

# replot (can you see the red colored node)
plot.igraph(graph,vertex.size=3,layout=layout.kamada.kawai, vertex.label.cex=0.5, vertex.label=NA)

# add node names
plot.igraph(graph,vertex.size=3,layout=layout.kamada.kawai, vertex.label.cex=0.5, vertex.label.dist=0.2)

# EXERCISE: try different graph layouts
# layout.fruchterman.reingold
# layout.mds
# layout.circle
# etc

# get degree for each node
degree(graph)

# histogram of degrees
hist(degree(graph))

# plot again
plot.igraph(graph,vertex.size=3,layout=layout.kamada.kawai, vertex.label.cex=0.5, vertex.label.dist=0.2)

# find clusters of nodes (connected components) 
cl <- clusters(graph)

# look at object
cl

# get a color pallete, one for each cluster
col <- rainbow(cl$no)

# assign color to node based on cluster membership
V(graph)$color <- col[cl$membership+1]

# plot
plot.igraph(graph, vertex.size=3,layout=layout.kamada.kawai, vertex.label.cex=0.5, vertex.label.dist=0.2)

# here we are going to remove isolated nodes

# #identify isolated nodes
bad.vs<-V(graph)[degree(graph) == 0] 

# remove isolated nodes
graph <-delete.vertices(graph, bad.vs)

# show remaining nodes
V(graph)

# show edges
E(graph)

# get connected components in a list
modules <- decompose.graph(graph)

# plot second component only
plot.igraph(modules[[ 1 ] ], layout=layout.kamada.kawai, vertex.label.dist=0.5)

# find largest connected component (module)
largest <- which.max(sapply(modules, vcount))

# plot largest module
plot(modules[[largest]], layout=layout.fruchterman.reingold, vertex.label.dist=0.5)

# EXERCISE: change correlation threshold to 0.6, redraw graph, find best layout

# install and lood library
install.packages("GeneNet")
library(GeneNet)

# partial correlation matrix
pcormat <- ggm.estimate.pcor(t(m))

#
t.edges <- ggm.test.edges(pcormat, plot=F)

# get network
t.net <- extract.network(t.edges, cutoff.ggm=0.9)

# look at it
t.net

# get igraph object
t.graph <- ggm.make.igraph(t.net, rownames(m))

# make 
plot.igraph(t.graph,vertex.size=3,layout=layout.kamada.kawai, vertex.label.cex=0.5)

# degree
degree(graph)

# exercise: make graph look better
# e.g. identify clusters, give each of them a color



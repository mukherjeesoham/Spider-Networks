#============================================================================
# Code to compute network metrics from adjacency matrix
# Soham Mukherjee 3/2017
#============================================================================

library(igraph)
library(viridis)
library(gplots)
library(ggplot2)
library(reshape2)
library(car)

rm(list = ls())
gc()

generate_GRAPH <- function(file, CC, ID)
{
	ADJ   <- as.matrix(read.csv(file, header=F))
	GRAPH <- graph.adjacency(ADJ, mode="directed", weight=TRUE)
	GRAPH <- simplify(GRAPH, remove.multiple = F, remove.loops = TRUE)
	GRAPH <- set_vertex_attr(GRAPH, "RETREAT", value=rep(c('gray8','gray87'), each=20))

	cat("\nWokring on file:", file)
	GRAPH  <- delete.vertices(GRAPH, degree(GRAPH)==0)		# delete isolates
}

compute_metrics <- function(GRAPH, ID)
{
	# aka. clustering coefficent
	TRANSITIVITY <- as.vector(transitivity(GRAPH, type="weighted", isolates='zero')) #giving NaN's
	BETWEENNESS  <- as.vector(betweenness(GRAPH, v=V(GRAPH), directed = TRUE, weights = E(GRAPH)$weight, nobigint = TRUE, normalized = FALSE))
	EIGENVECTOR  <- as.vector(evcent(GRAPH, scale = TRUE, weights = E(GRAPH)$weight)$vector)
	
	# Parameters we really look for
	NODE_STRENGTH  <- as.vector(graph.strength(GRAPH, mode = 'all', weights = E(GRAPH)$weight))
	NODE_DEGREE    <- degree(GRAPH, mode = 'all')
	EDGE_WEIGHT	   <- E(GRAPH)$weight

	# Store them in an array called metrics
	METRICS <- cbind(seq(1,40,1), TRANSITIVITY, BETWEENNESS, EIGENVECTOR, NODE_STRENGTH, NODE_DEGREE)

	colnames(METRICS) <- c("ID","TRANSITIVITY", "BETWEENNESS", "EIGENVECTOR", "NODE_STRENGTH", "NODE_DEGREE")
	write.table(METRICS, file = sprintf('../output/metrics/metrics_%s.csv', gsub(".csv", "", ID)), sep=",", row.names=FALSE)
	
    # Separately store a file which contains the edgeweight distribution
    write.table(EDGE_WEIGHT, file = sprintf('../output/metrics/edgeweights_%s.csv', gsub(".csv", "", ID)), sep=",", row.names=FALSE, col.names='EDGE_WEIGHT')
	
    RESULT <- METRICS
}

#=================================================================
# Control Panel
#=================================================================

# read the location of the files and the the location for the color codes.
file.names <- dir('../output/csv/ADJ', pattern ="*.csv")
system("mkdir -p ../output/metrics")

for (i in 1:length(file.names))
{	
	file   <- sprintf('../output/csv/ADJ/%s', file.names[i])
	GRAPH  <- generate_GRAPH(file, CC, file.names[i])
	compute_metrics(GRAPH, file.names[i])
}	
cat("\n")

# read the location of the random dataset files.
file.names <- dir('../output/csv/ADJ/random', pattern ="*.csv")

for (i in 1:length(file.names))
{	
	file   <- sprintf('../output/csv/ADJ/random/%s', file.names[i])
	GRAPH  <- generate_GRAPH(file, CC, file.names[i])
	compute_metrics(GRAPH, file.names[i])
}	
cat("\n")

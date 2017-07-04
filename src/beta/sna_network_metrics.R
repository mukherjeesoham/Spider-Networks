library(viridis)
library(ggplot2)
library(gplots)

generate_GRAPH <- function(file)
{
	ADJ <- read.csv(file, header=F)
	ADJ <- as.matrix(ADJ)
	G <- graph.adjacency(ADJ, mode="directed", weight=TRUE)
	GRAPH <- simplify(G, remove.multiple = F, remove.loops = T)
}

plot_distribution <-function(DATA)
{
	#needs major fixing : not of primary importance.
	dat <- data.frame(treatment = factor(rep(c("DC","SCDR", "SCSR"), each=40)), degree = c(D_DC, D_SCDR, D_SCSR))
	d <- ggplot(dat, aes(x=degree, fill=treatment)) + geom_histogram(binwidth=0.1, alpha=0.3, position="identity")

	ggsave('all_degree_histogram.pdf', d)

	c <- ggplot(dat, aes(x=degree, colour=treatment)) + geom_density()
	ggsave('all_degree_density.pdf', c)
}

node_metrics <- function(GRAPH, ID)
{
	BETWEENNESS    <- as.vector(betweenness(GRAPH, v=V(GRAPH), directed = TRUE, weights = E(GRAPH)$weight, nobigint = TRUE, normalized = FALSE))
	NODE_STRENGTH  <- as.vector(graph.strength(GRAPH, mode = 'all', weights = E(GRAPH)$weight))
	NODE_DEGREE    <- as.vector(degree(GRAPH, mode = 'all')
	EIGENVECTOR    <- as.vector(evcent(GRAPH, scale = TRUE, weights = E(GRAPH)$weight)$vector)
	RANK           <- read.csv(sprintf('/Users/apple/Documents/Network_Analysis/Playground/output/T_Rank/%s', ID), header=F)

	#----------------------------------------------------------------------------------
	RB <- data.frame(RANK, BETWEENNESS)
	pdf(file = sprintf('/Users/apple/Documents/Network_Analysis/Playground/output/visualisations/correlations/RB_%s.pdf', gsub(".csv", "", ID)))
	plot(RB, pch=19, cex=1, col="orange", xlab="Rank", ylab="Betweenness", main=gsub(".csv", "", ID))
	dev.off()


	RN <- data.frame(RANK, NODE_STRENGTH)
	pdf(file = sprintf('/Users/apple/Documents/Network_Analysis/Playground/output/visualisations/correlations/RN_%s.pdf', gsub(".csv", "", ID)))
	plot(RN, pch=19, cex=1, col="orange", xlab="Rank", ylab="Node strength", main=gsub(".csv", "", ID))
	dev.off()

	RE <- data.frame(RANK, EIGENVECTOR)
	pdf(file = sprintf('/Users/apple/Documents/Network_Analysis/Playground/output/visualisations/correlations/RE_%s.pdf', gsub(".csv", "", ID)))
	plot(RE, pch=19, cex=1, col="orange", xlab="Rank", ylab="EigenVector centrality", main=gsub(".csv", "", ID))
	dev.off()

	#----------------------------------------------------------------------------------

	METRICS <- cbind(seq(1,40,1), BETWEENNESS, NODE_STRENGTH, NODE_DEGREE, EIGENVECTOR, RANK)
	colnames(METRICS) <- c("ID", "BETWEENNESS", "NODE_STRENGTH", "NODE_DEGREE", "EIGENVECTOR", "RANK")
	write.table(METRICS, file = sprintf('/Users/apple/Documents/Network_Analysis/Playground/output/metrics/metrics_%s.csv', gsub(".csv", "", ID)), sep=",", row.names=FALSE)
	RESULT <- METRICS
}

CC <- read.csv("/Users/apple/Documents/Network_Analysis/Playground/data/color_coding.csv")
pallete <- viridis(1000.0, alpha = 1, begin = 0, end = 1, option = "D")
file  <- '/Users/apple/Documents/Network_Analysis/Playground/output/metrics/metrics_R_SCSR_F09.csv'

DATA <- as.matrix(read.csv(file))
plot_distribution(DATA)

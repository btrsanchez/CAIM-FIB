#Leer el grafo asegurandose de que sea no dirigido
g <- read.graph("edges.txt",directed = FALSE)

#visualizar el grafo
plot(g)

#vertices, aristas, diametro y transitividad 
V(g)
E(g)
diameter(g,directed=FALSE)
transitivity(g)

#grado de distribucion
degree(g)
degree.distribution(g)
max(degree.distribution(g))
hist(degree(g),breaks=30)

#Tamaño equivalente al pagerank
c=(page.rank(g)$vector)*500
plot(g,vertex.size=c)

#community detection
wal <- walktrap.community(g)
plot(wal, g)

#Histograma tamaño comunidades
sizes(wal)
plot(sizes(wal))

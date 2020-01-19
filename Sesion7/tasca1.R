# Task 1
p <- 10^(seq(-4,0,0.2))

trans <- c(1)
path <- c(1)

for(i in p)
{
  graph <- watts.strogatz.game(1, 1000, 4, i)
  trans <- c(trans, transitivity(graph))
  path <- c(path, average.path.length(graph))
}

#delete auxiliar values
trans <- trans[-1]
path <- path[-1]

#normalized to be within the range [0, 1]
trans <- trans/trans[1]
path <- path/path[1]

plot(p, trans, ylim = c(0,1), log="x", ylab="coeff") 
points(p,path, pch=16)
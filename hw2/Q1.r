
library("igraph")
library(repr)
options(repr.plot.width=4, repr.plot.height=4)
colors = c("red", "yellow", "green", "violet", "orange", "blue", "pink", "cyan")

# Implementation of Random Walk, with teleportation
rwalk = function(g, start, ncount) {
    node = start
    path = rep(NA, ncount)
    path[[1]] = node
    i = 2 

    while(i <= ncount) {
        neigh = neighbors(g, node)
        if(length(neigh) == 0){
                node = sample.int(vcount(g), 1)
        } else {
                node = sample(neigh, 1)
        }

        path[[i]] = node
        i = i + 1
    }
    
    path
}


random_walker <- function(nv, probability) {
    g = random.graph.game(n = nv, p = probability, directed = FALSE)
    cat("Network with", nv, "nodes and diameter", diameter(g))

    average_step_t = c()
    average_standard_deviation_t = c() 
    distance_matrix = shortest.paths(g, v = V(g), to = V(g))
    deg_random_walk = c()
    
    for(t in 1 : 50) {
        distance = numeric()
        cat(t)
        
        # Do a random walk starting from all vertices
        for(v in sample.int(vcount(g), 25)) {
            walk = rwalk(g, v, t)
            start_vertex = v
            tail_vertex  = tail(walk, 1)
            
            shortest_distance = distance_matrix[start_vertex, tail_vertex]
            if (shortest_distance == Inf) {
                shortest_distance = 0
            }
            distance = c(distance, shortest_distance)
            deg_random_walk = c(deg_random_walk, degree(g, v = tail_vertex)) 
        }
        average_step_t = c(average_step_t, mean(distance))
        average_standard_deviation_t = c(average_standard_deviation_t, mean((distance - mean(distance))**2))    
    }
    
    return(
        list("s(t)" = average_step_t, 
             "sigma(t)" = average_standard_deviation_t, 
             "d(all)" = degree(g, mode="all"),
             "d(end)" = deg_random_walk
        )
    )
}

plot_average_path_length = function(W, vmax) {
    plot(
        1 : 50, 
        W$`s(t)`, 
        type="l", 
        xlab="Number of steps(t)", 
        ylab = "Average Path length <s(t)>",
        ylim = c(0, vmax),
        main = "Plot of average path length"
    )
}

plot_sd_path_length = function(W, vmax) {
    plot(
        1 : 50, 
        W$`sigma(t)`, 
        type="l", 
        xlab="Number of steps(t)", 
        ylab = "Standard deviation",
        ylim = c(0.0, vmax),
        main = "Plot of standard deviation of path length"
    )
}

W1000 = random_walker(1000, 0.01)

plot_average_path_length(W1000, 3.5)

plot_sd_path_length(W1000, 1)

cat("Mean s(t) is ", mean(W1000$`s(t)`))

cat("Mean sigma(t) is ", mean(W1000$`sigma(t)`))

hist(
    W1000$`d(all)`, 
    col=colors,
    main="Degree distribution of full graph",
    xlab="Vertex degrees",
    ylab="Vertex count"
)

hist(
    W1000$`d(end)`, 
    col=colors,
    main="Degree distribution of end points of walks",
    xlab="Vertex degrees",
    ylab="Vertex count"
)

W100 = random_walker(100, 0.01)

plot_average_path_length(W100, 1)

plot_sd_path_length(W100, 5)

W = random_walker(10000, 0.01)

plot_average_path_length(W, 5)

plot_sd_path_length(W, 1.0)

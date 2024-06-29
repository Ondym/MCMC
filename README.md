# MCMC

Here are the files created during the TV@J within the MCMC miniproject. The results and the math behind the contents of this repository are [here](https://tydenvedy.fjfi.cvut.cz/fyztyd/fyztyd/uploadsb/files/montemarkov_xx_180624_2316.pdf).

## The idea behind the project

This project deals with the problem of sampling from a predetermined Boltzmann distribution (Ising model) and analyzing it to answer the given questions using Monte Carlo and Markov chains (MCMC for short). 

## The problems to solve

1. Plot the dependence of the average energy on temperature.
2. Let _C_ be the number of connected black regions. Plot the
dependence of the expected value of _C_ and the temperature.
3. Let _L_ be the probability of percolations (forming of clusters
and their subsequent possibility of forming a chain connecting
the top and bottom, see the image lower). Plot this value with respect
to temperature. 

![Example of a square with the percolation highlighted.](/imgs/perkolace.png)

## The results

We processed the results by forgetting the first 10% of 10 million iterations. Individualaverages are indicated by points in the graphs, the shaded areas indicate the standarddeviation at each point.

In solving the first problem we obtained, using a special code, the relation in the image lower which shows a rapid increase in energy at the boundary of low and higher temperatures and then a much slower growth in the high and low temperatures respectively. In the second problem we attained the graph in Figure 7. We can see that the growth is very similar to the previous curve so they must be related. Lastly, in the third problem we got a much less clear result. However, we can still make out a apparent decrease in percolation probability with temperature. 
![12 final states with growing temperature](imgs/deconstructed-gif.png)
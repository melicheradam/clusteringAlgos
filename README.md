# clusteringAlgos

Implementations & testing of K-means, K-medoids, Divisive and Agglomerative clustering algorithms.

## K-means

This algorithm is that the points are assigned to the "averages" of the clusters, which are calculated from the average sum of the coordinates of all the points in the cluster. These centers are recalculated until the iteration takes place without changing the assignment of any point from our set of points, which means that the solution converged to the local optimum. 

<img src="https://user-images.githubusercontent.com/20504361/154844668-4270ac85-ab0d-42c8-be22-1d21c80e3f52.gif" style="width:45%;"> <img src="https://user-images.githubusercontent.com/20504361/154844672-3062c236-2f04-400b-8adf-f6c713181bdd.gif" style="width:45%">


## K-medoids

The algorithm is similar to K-means, except that the points are not assigned to the "average" of the clusters but to their most central point. At the beginning, the centers are also randomly initialized and assigned points. However, then the recalculation of the new potential centers is performed, and the point with the smallest distance from all the others in the cluster is selected as the new center. This process is also repeated until the iteration occurs without a new assignment. 

<img src="https://user-images.githubusercontent.com/20504361/154844708-63f1dd17-762a-48f7-82e5-3e9bbc22b54e.gif" style="width:45%;"> <img src="https://user-images.githubusercontent.com/20504361/154844713-25155117-74cd-475e-8ac9-3649cf8d08ab.gif" style="width:45%">


## Agglomerative clustering

Agglomerative clustering is a type of hierarchical clustering that goes from the bottom up. At the beginning of the algorithm, each point is a separate cluster, and each iteration of the algorithm merges the two nearest clusters. The distance between the two clusters can be determined in different ways, I chose Single-linkage, which means that the distance between the two clusters determines the smallest distance between their points. 

<img src="https://user-images.githubusercontent.com/20504361/154844779-b4ca10be-250f-418b-8df9-d2906d087f7f.png" style="width:45%;"> <img src="https://user-images.githubusercontent.com/20504361/154844782-8b55a1e4-633c-4608-a01f-71e01e108ac1.gif" style="width:45%">


## Divisive clustering

Divisional clustering works on the opposite principle as agglomerative. This approach initially treats all points as a single cluster, which is then divided into smaller parts. By using the K-means algorithm for cluster division, an efficient solution is achieved. I always share the cluster with the most points. 

<img src="https://user-images.githubusercontent.com/20504361/154844821-9c70a5bf-cf93-4df5-bfbe-9f2c3d937e37.gif" style="width:45%;"> <img src="https://user-images.githubusercontent.com/20504361/154844826-32e177e0-dba4-49fd-b805-264a0049cc60.gif" style="width:45%">


## Comparison

The graphs below show the trend of decreasing / increasing time intensity with the change of the parameter k. Each algorithm was run at 20,000 points, except for the agglomerative, which was run at only 1,000 points. We see that in the agglomerative clustering, parameter k does not play a role at all. This is because the algorithm iterates n minus k times, so there is only a small difference. However, with K-Means and Division, the trend is increasing, which is again understandable, because the algorithms have to iterate several times, but this time the parameter has more weight. With the K-Medoid algorithm, the trend is declining, because when there are few large clusters, it has to swap many times before the solution converges. 

<img src="https://user-images.githubusercontent.com/20504361/154845150-3160847f-4a56-4582-8524-87fb2c5371de.png" style="width:45%;"> <img src="https://user-images.githubusercontent.com/20504361/154845163-ec8d3a31-6331-4dc1-a960-639adff7f6fc.png" style="width:45%">

<img src="https://user-images.githubusercontent.com/20504361/154845170-11b6ad40-6941-4540-8a89-6df743c22c57.png" style="width:45%;"> <img src="https://user-images.githubusercontent.com/20504361/154845182-e4346915-98cf-4368-97c6-c027561cf995.png" style="width:45%">

By far the best algorithm is K-Means. It is fast and gives relatively good splits. The best distribution was given by the Agglomerative approach, but at a huge time cost, so it cannot be considered effective. Divisional clustering was also nice, but because it always divides clusters, and can not exchange points between clusters does not search a large enough state space. At least not always. K-medoids was the worst, lasting too long for the results. 



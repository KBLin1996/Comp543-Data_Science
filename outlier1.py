import heapq as hq
import numpy as np
import time


if __name__ == '__main__':
    # Create the covariance matrix
    covar = np.zeros((100,100))
    np.fill_diagonal(covar, 1)

    # And the mean vector
    mean = np.zeros(100)

    # Create 3000 data points
    all_data = np.random.multivariate_normal(mean, covar, 3000)

    # Now create the 20 outliers
    for i in range(1, 20):
        mean.fill(i)
        outlier_data = np.random.multivariate_normal(mean, covar, i)
        all_data = np.concatenate((all_data, outlier_data))

    # k for kNN detection
    k = 10

    # The number of outliers to return
    m = 5

    # Start the timer
    start_time = time.time()

    # The priority queue of outliers
    outliers = list()

    #YOUR CODE HERE!
    outliersDict = dict()
    for idx, i in enumerate(all_data):
        maxPriority = list()
        hq.heapify(maxPriority)
        for jdx, j in enumerate(all_data):
            if idx == jdx:
                continue
            hq.heappush(maxPriority, -np.linalg.norm(j - i))
            if len(maxPriority) > k:
                hq.heappop(maxPriority)
        # Insert idx into with key max(maxPriority)
        outliersDict[-hq.heappop(maxPriority)] = idx

        if len(outliersDict) > m:
            minPriority = list(outliersDict.keys())
            hq.heapify(minPriority)
            outlierKey = hq.heappop(minPriority)
            del outliersDict[outlierKey]

    # Get key by dict() value
    for key, value in outliersDict.items():
        outliers.append((key, value))

    print("--- %s seconds ---" % (time.time() - start_time))

    # Print the outliers... 
    for outlier in outliers:
        print(outlier)

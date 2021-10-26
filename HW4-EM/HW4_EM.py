import numpy as np
import scipy.stats

def EstimateCoinHeadCnt(flips):
    # One coin has a probability of coming up heads of 0.2, the other 0.6
    coinProbs = np.zeros(2)
    coinProbs[0] = 0.2
    coinProbs[1] = 0.6

    # Reach in and pull out a coin numTimes times
    numTimes = 100

    # Flip it numFlips times when you do
    numFlips = flips

    # Flips will have the number of heads we observed in 10 flips for each coin
    flips = np.zeros(numTimes)

    for coin in range(numTimes):
        # which is a one-dimensional numpy array
        which = np.random.binomial(1, 0.5, 1);
        # How many times did the unknown coin show head when I flipped it 10 times
        flips[coin] = np.random.binomial(numFlips, coinProbs[which], 1);


    # Initialize the EM algorithm
    coinProbs[0] = 0.79
    coinProbs[1] = 0.51

    # Run the EM algorithm
    for iters in range (20):
        estimateHeadCntA = 0
        estimateHeadCntB = 0
        estimateTailCntA = 0
        estimateTailCntB = 0

        for flipIdx in range(numTimes):
            headCnt = flips[flipIdx]
            tailCnt = numFlips - headCnt
            coinA = (coinProbs[0] ** headCnt) * ((1 - coinProbs[0]) ** tailCnt)
            coinB = (coinProbs[1] ** headCnt) * ((1 - coinProbs[1]) ** tailCnt)
            coinAProb = coinA / (coinA + coinB)
            #coinBProb[flipIdx] = coinB / (coinA + coinB)
            coinBProb = 1 - coinAProb

            estimateHeadCntA += coinAProb * headCnt
            estimateTailCntA += coinAProb * tailCnt
            estimateHeadCntB += coinBProb * headCnt
            estimateTailCntB += coinBProb * tailCnt

        coinProbs[0] = estimateHeadCntA / (estimateHeadCntA + estimateTailCntA)
        coinProbs[1] = estimateHeadCntB / (estimateHeadCntB + estimateTailCntB)
        print(coinProbs)


if __name__ == '__main__':
    print("numFlips: 10")
    EstimateCoinHeadCnt(10)
    print("\nnumFlips: 2")
    EstimateCoinHeadCnt(2)

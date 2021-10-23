import math
import numpy as np


def f(x, y):
    return math.sin(x+y) + (x-y) ** 2 - 1.5*x + 2.5*y + 1

def dfx(x, y):
    return math.cos(x+y) + 2 * (x-y) - 1.5

def dfy(x, y):
    return math.cos(x+y) - 2 * (x-y) + 2.5

def dfx2(x, y):
    return -math.sin(x+y) + 2

def dfy2(x, y):
    return -math.sin(x+y) + 2

def dfxfy(x, y):
    return -math.sin(x+y) - 2

def gd_optimize(a):
    learningRate = 1.0
    lossPrev = abs(f(a[0], a[1]))
    lossDiff = 1.0
    resultCur = np.zeros(2)
    resultPrev = a

    while(abs(lossDiff) > 10e-20):
        resultCur = resultPrev - learningRate * np.array([dfx(resultPrev[0], resultPrev[1]), dfy(resultPrev[0], resultPrev[1])])

        lossCur = f(resultCur[0], resultCur[1])
        print(lossCur)

        lossDiff = lossCur - lossPrev
        # If the value of the loss increases in an iteration, then we half the learning rate
        if(lossDiff > 0):
            learningRate *= 0.5
        # If the value of the loss decreases in an iteration, then we multiply 1.1 on the learning rate
        else:
            learningRate *= 1.1

        lossPrev = lossCur
        resultPrev = resultCur
    print(resultCur)

def procedurenm_optimize(a):
    lossPrev = abs(f(a[0], a[1]))
    lossDiff = 1.0
    resultCur = np.zeros(2)
    resultPrev = np.transpose(a)

    while(abs(lossDiff) > 10e-20):
        x = resultPrev[0]
        y = resultPrev[1]
        resultCur = resultPrev - np.dot(np.linalg.inv([[dfx2(x, y), dfxfy(x, y)], [dfxfy(x, y), dfy2(x, y)]]),
                                        np.transpose([dfx(x, y), dfy(x, y)]))
        lossCur = f(resultCur[0], resultCur[1])
        print(lossCur)

        lossDiff = lossCur - lossPrev
        lossPrev = lossCur
        resultPrev = resultCur
    print(resultCur)


if __name__ == '__main__':
    print(">>> gd_optimize(np.array([-0.2, -1.0]))")
    gd_optimize(np.array([-0.2, -1.0]))
    print("\n>>> gd_optimize(np.array([-0.5, -1.5]))")
    gd_optimize(np.array([-0.5, -1.5]))
    print("\n\n>>> procedurenm_optimize(np.array([-0.2, -1.0]))")
    procedurenm_optimize(np.array([-0.2, -1.0]))
    print("\n>>> procedurenm_optimize(np.array([-0.5, -1.5]))")
    procedurenm_optimize(np.array([-0.5, -1.5]))

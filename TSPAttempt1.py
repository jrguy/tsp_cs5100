# Based on description from Sanford Assignment Here
'''
  https://www.web.stanford.edu/class/cs168/p7.pdf

'''

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import copy


N = 16 # the number of cities

# simulate an adjacency matrix of distances
distance = np.random.rand(N, N)
distance = (distance + distance.T) / 2.0
ind_diag = range(N)
distance[ind_diag, ind_diag] = 0

# Calculate total distance for a given sequence
def cal_dist(distance, L):
    d = 0
    for i in range(len(L)):
        d = d + distance[L[i % N], L[(i + 1) % N]]
    return d

def findMinimFour(AdjacencyList):
    '''
      findMinimFour returns a list of lists that for each for of the adj. list
      contains a list of the four minimum connections in order for a given row,
      including the indices involved, then the cost, then the rank for the item.
      This necessarily entails looping over the entire set twice in the brute
      force method. Better methodologies for determining the minimum four of the
      unsorted set would be needed in such a way that the original values are not
      perturbed. At end returns the set of such combinations for the adj. list
    '''
    listOfFourBestByRow = []
    for i in range(len(AdjacencyList)):
        currentRow = []
        leastMin = math.inf
        secondLeastMin = math.inf
        thirdLeastMin = math.inf
        fourthLeastMin = math.inf
        indexSetLeast = []
        indexSetSecondLeast = []
        indexSetThirdLeast = []
        indexSetFourthLeast = []
        for j in range(len(AdjacencyList[i])):
            if i == j:
                continue # No need to do the zero entries
            else:
                if AdjacencyList[i][j] < leastMin and len(indexSetLeast)==0:
                    indexSetLeast = [i, j]
                    leastMin = AdjacencyList[i][j]
                elif AdjacencyList[i][j] < leastMin and len(indexSetLeast) == 2:
                    if len(indexSetSecondLeast) == 0:
                        indexSetSecondLeast = [indexSetLeast[0], indexSetLeast[1]]
                        secondLeastMin = leastMin
                        leastMin = AdjacencyList[i][j]
                        indexSetLeast = [i, j]
                    elif len(indexSetSecondLeast) == 2:
                        if len(indexSetThirdLeast) == 0:
                            indexSetThirdLeast = [indexSetSecondLeast[0], indexSetSecondLeast[1]]
                            thirdLeastMin = secondLeastMin
                            indexSetSecondLeast = [indexSetLeast[0], indexSetLeast[1]]
                            secondLeastMin = leastMin
                            leastMin = AdjacencyList[i][j]
                            indexSetLeast = [i, j]
                        elif len(indexSetThirdLeast) == 2:
                            indexSetFourthLeast = [indexSetThirdLeast[0], indexSetThirdLeast[1]]
                            fourthLeastMin = thirdLeastMin
                            indexSetThirdLeast = [indexSetSecondLeast[0], indexSetSecondLeast[1]]
                            thirdLeastMin = secondLeastMin
                            indexSetSecondLeast = [indexSetLeast[0], indexSetLeast[1]]
                            secondLeastMin = leastMin
                            leastMin = AdjacencyList[i][j]
                            indexSetLeast = [i, j]
                elif AdjacencyList[i][j] < secondLeastMin and len(indexSetSecondLeast) == 0:
                    indexSetSecondLeast = [i, j]
                    secondLeastMin = AdjacencyList[i][j]
                elif AdjacencyList[i][j] < secondLeastMin and len(indexSetSecondLeast) == 2:
                    if len(indexSetThirdLeast) == 0:
                        indexSetThirdLeast = [indexSetSecondLeast[0], indexSetSecondLeast[1]]
                        thirdLeastMin = secondLeastMin
                        indexSetSecondLeast = [i, j]
                        secondLeastMin = AdjacencyList[i][j]
                    elif len(indexSetThirdLeast) == 2:
                        indexSetFourthLeast = [indexSetThirdLeast[0], indexSetThirdLeast[1]]
                        fourthLeastMin = thirdLeastMin
                        indexSetThirdLeast = [indexSetSecondLeast[0], indexSetSecondLeast[1]]
                        thirdLeastMin = secondLeastMin
                        indexSetSecondLeast = [i, j]
                        secondLeastMin = AdjacencyList[i][j]
                elif AdjacencyList[i][j] < thirdLeastMin and len(indexSetThirdLeast) == 0:
                    indexSetThidLeast = [i, j]
                    thirdLeastMin = AdjacencyList[i][j]
                elif AdjacencyList[i][j] < thirdLeastMin and len(indexSetThirdLeast) == 2:
                    indexSetFourthLeast = [indexSetThirdLeast[0], indexSetThirdLeast[1]]
                    fourthLeastMin = thirdLeastMin
                    thirdLeastMin = AdjacencyList[i][j]
                    indexSetThirdLeast = [i, j]
                elif AdjacencyList[i][j] < fourthLeastMin :
                    indexSetFourthLeast = [i, j]
                    fourthLeastMin = AdjacencyList[i][j]
                else:
                    continue
                # End chained set
            # End outer chain component loop goes to next j value here
        # Exit J For Loop, no return here, but update larger set
        currentRowOpportunityCost = (fourthLeastMin + thirdLeastMin) - (secondLeastMin + leastMin)
        currentRow = [leastMin, indexSetLeast[0], indexSetLeast[1],
                      secondLeastMin, indexSetSecondLeast[0], indexSetSecondLeast[1],
                      thirdLeastMin, indexSetThirdLeast[0], indexSetThirdLeast[1],
                      fourthLeastMin, indexSetFourthLeast[0], indexSetFourthLeast[1], "currentRow Opportunity Cost: ", currentRowOpportunityCost]
        listOfFourBestByRow.append(currentRow)
    # Exit I for Loop, return should be at this indent
    return listOfFourBestByRow
# The exit point

bestFourByRowOfAdjacencyMatrix = findMinimFour(distance)
print("Current Adjacency Matrix Below ")
for row in range(len(distance)):
    print(distance[row])
print("\n")
print("Best 4 neighbors in adjacency matrix below ")
for row in bestFourByRowOfAdjacencyMatrix:
    print(row)
print("\n")

def simulateSet(numberOfSimulations:int=10, TVal:int = -1):
    setOfBestDistances = []
    setOfBestPaths = []
    for j in range(numberOfSimulations):
        if TVal == -1:
            T = 1000
        else:
            T = TVal
        ITER = 100000
        L = np.arange(N)
        print("Original L  and distance: ", L)
        best = L
        bestDistance = cal_dist(distance, L)
        print (cal_dist(distance, L)) # initial distance
        dist_all = []
        for i in range(ITER):
            a = np.random.randint(1, N - 1) # Pick a random value in range for your set
            d_t = cal_dist(distance, L) # Get the distance you currently have
            dist_all.append(d_t) # Put this in the list that will track distance over time
            L_tmp = copy.copy(L) # Make a copy
            L_tmp[[a, (a + 1)%N]] = L_tmp[[(a + 1)%N, a]] # Set the L_temp at the position and position+1 modulo N to the value at position+1 module N and position (does the swap of the value positions)
            L_tmp_dist = cal_dist(distance, L_tmp) # Get the distance of the new temporary form (don't know if you'll keep it yet or not)
            delta_d = cal_dist(distance, L_tmp) - d_t # Get the distance of the new set up
            if delta_d < 0 or ( T > 0 and random.random() < math.exp(-1*delta_d/T)): # Make a decision based on either improvement, or based on random selection
                L = L_tmp
            if d_t < bestDistance:
                best = L_tmp
                bestDistance = cal_dist(distance, L_tmp)
            if T > 3:
                T -= 2
            else:
                T = float(T) / (float(i)+(1.0*(TVal+1)))
        print("Final L and distance : ", L)
        finalDistance = cal_dist(distance, L)
        print (finalDistance) # final distance
        plt.plot(dist_all)
        setOfBestDistances.append(finalDistance)
        setOfBestPaths.append(L)
    minDist = min(setOfBestDistances)
    bestPath = setOfBestPaths[setOfBestDistances.index(minDist)]
    print("After ", numberOfSimulations, " the best path and distance found below")
    print(minDist)
    print(bestPath)

def simulateBiggerGroupsOfSets(numberOfSimulations:int = 10):
    # Couple rounds of tests later and there seems to be a discrepancy towards
    # different temperatures. Varying temperature may be more effective in the long run.
    # Seems to be somewhere above 10 and below 10000, which is a range to be sure.
    # Also may be that different temperatures work better for different set ups as well.
    # TList = [0, 1, 10, 100, 1000, 10000, 50000, 100000]
    TList = [10, 100, 1000]
    for k in range(len(TList)):
        print("Results for T = ", TList[k])
        simulateSet(10, TList[k])
        print("End Results for set \n\n")

simulateBiggerGroupsOfSets()
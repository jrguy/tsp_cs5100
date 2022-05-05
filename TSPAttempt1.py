# Based on description from Sanford Assignment Here
'''
  https://www.web.stanford.edu/class/cs168/p7.pdf

'''

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import copy

# Given an adjacency matrix, row number -> return tuple of rows in chain if promising or False
# For a given row, determine if there exists a promising chain by
# First, get cost of chain B-A-C and find difference with NOTB,C - A - NOTB,C2
# Then, get cost of NOTA,C - B - NOTA,C and find difference with A-B-NOTA,C
# Do same with C : NOTA,B - C - NOTA,B and find difference with A-C-NOTA,B
# Record both of these, and sum with initial value.
# Then get cost of A-B-C and find difference with A-B-NOTA,C. If negative, can discard -> implies clique forming
# Do not sum with initial.
# Do same for A-C-B and find difference with A-C-NOTA,B. If negative, can discard -> implies clique forming
# Do not sum with initial.
# We do not sum non-clique forming as that is to be expected of promising chains.

def promising_sequence(adjacencyMatrix, rowNum):
    # Get minimum indices and values for the stated rowNumber
    # Get minimum indices and values for the paired rows not including each other
    # Do analysis
    # For now, assume undirected graph for adjacency matrix
    minB = math.inf
    minC = math.inf
    indexB=[rowNum, -1]
    indexC=[rowNum, -1]
    # Loop through and get the minimum B and C for the set up, as well as their
    # matrice locations. Note that you will then use the second value as the
    # row value for these going forward.
    for j in range(len(adjacencyMatrix[rowNum])):
        if j == rowNum:
            continue
        else:
            if minB > adjacencyMatrix[rowNum][j]:
                if minB == math.inf:
                    minB = adjacencyMatrix[rowNum][j]
                    indexB = [rowNum, j]
                else:
                    minC = minB
                    indexC = [rowNum, indexB[1]]
                    minB = adjacencyMatrix[rowNum][j]
                    indexB = [rowNum, j]
    # Now we can go and get the mins for B and for C that are not A, B and A, C
    Bmin1=math.inf
    Bmin2=math.inf
    BIndexList1 = [indexB[1], -1]
    BIndexList2 = [indexB[1], -1]
    Cmin1=math.inf
    Cmin2=math.inf
    CIndexList1 = [indexC[1], -1]
    CIndexList2 = [indexC[1], -1]
    # Do B first
    for j in range(len(adjacencyMatrix[indexB[1]])):
        if j == indexB[1] or j == rowNum or j == indexC[1]:
            continue # Don't match these ones
        else:
            if Bmin1 > adjacencyMatrix[indexB[1]][j]:
                if Bmin1 == math.inf:
                    Bmin1 = adjacencyMatrix[indexB[1]][j]
                    BIndexList1 = [indexB[1], j]
                else:
                    Bmin2 = Bmin1
                    BIndexList2 = [indexB[1], BIndexList1[1]]
                    Bmin1 = adjacencyMatrix[indexB[1]][j]
                    BIndexList1 = [indexB[1], j]

    # Similarly now for C
    for j in range(len(adjacencyMatrix[indexC[1]])):
        if j == indexB[1] or j == rowNum or j == indexC[1]:
            continue # Don't match these ones
        else:
            if Cmin1 > adjacencyMatrix[indexC[1]][j]:
                if Cmin1 == math.inf:
                    Cmin1 = adjacencyMatrix[indexC[1]][j]
                    CIndexList1= [indexC[1], j]
                else:
                    Cmin2 = Cmin1
                    CIndexList2 = [indexC[1], CIndexList1[1]]
                    Cmin1 = adjacencyMatrix[indexC[1]][j]
                    CIndexList1 = [indexC[1], j]

    # Once more for A but now without B and C. Condense this later.
    AaltMin1 = math.inf
    AaltMin2 = math.inf
    Aalt1Index = [rowNum, -1]
    Aalt2Index = [rowNum, -1]
    for j in range(len(adjacencyMatrix[rowNum])):
        if j == rowNum or j == indexB[1] or j == indexC[1]:
            continue # Don't match these ones
        else:
            if AaltMin1 > adjacencyMatrix[rowNum][j]:
                if AaltMin1 == math.inf:
                    AaltMin1 = adjacencyMatrix[rowNum][j]
                    Aalt1Index[1] = j
                else:
                    AaltMin2 = AaltMin1
                    Aalt2Index=[rowNum, Aalt1Index[1]]
                    AaltMin1 = adjacencyMatrix[rowNum][j]
                    Aalt1Index=[rowNum, j]

    # 1) Weight of A with not b or c 1 and not b or c 2
    # 2) Weight of A with b and c
    # 3) Weight of B with not A or C
    # 4) Weight of C with not A or B
    # 5) Weight of B with A and not C
    # 6) Weight of C with A and not B
    # 1 - 2 -> Cost of A not getting B or C (costTotal1)
    # 3 - 5 -> Cost of B not getting A (costTotal2)
    # 4 - 6 -> Cost of C not getting A (costTotal3)
    # 2 - 5 -> Cost of Clique  -> Ignored if negative or 0 (cliqueCheck1)
    # 2 - 6 -> Cost of Clique  -> Ignored if negative or 0 (cliqueCheck2)
    weightAwithoutBC = AaltMin1+AaltMin2
    weightAwithBC = minB + minC
    costTotal1 = weightAwithoutBC - weightAwithBC
    weightOfBwithoutAC = Bmin1 + Bmin2
    weightOfCwithoutAB = Cmin1 + Cmin2
    weightOfBwithAnotC = minB + Bmin1
    weightOfCwithAnotB = minC + Cmin1
    costTotal2 = weightOfBwithoutAC - weightOfBwithAnotC
    costTotal3 = weightOfCwithoutAB - weightOfCwithAnotB
    costTotal1 += costTotal2 + costTotal3
    cliqueCheck1 = weightAwithBC - weightOfBwithAnotC
    cliqueCheck2 = weightAwithBC - weightOfCwithAnotB

    # [IsPromising, [centralOrOriginalNode], [nodesOntheLeft], [nodesOnTheRight], promisingValue]

    if cliqueCheck1 < 0 or cliqueCheck2 < 0 :
        # Avoid cliques
        return [False, rowNum, indexB[1], indexC[1], costTotal1]
    else:
        if costTotal1 < 0:
            # Avoid non promising chains
            return [False, rowNum, indexB[1], indexC[1], costTotal1]
        else:
            return [True, rowNum, indexB[1], indexC[1], costTotal1] # These form a promising chain

def join_chains(true_chains):
    '''
      true_chains is a list of chains of form [trueValue, originNode, leftNode, rightNode, promisingValue]
      join_chains is going to go through the list of true chains and find any that have matches and could be joined or must be resolved as conflicts
      consider if originNode is A, leftNode is B, and rightNode is C
      We then need to scan through true_chains for any chains that have an originNode of B or C
      These would then be of the form
      originNode B, leftNode is Vi, rightNode is Vj
      originNode C, leftNode is Vk, rightNode is Vl
      where Vijkl are the different node possibilities for left and right for each
      For the case of originNodeB
        If Vi or Vj is A, then we can join. But if Vi and Vj are not A, then we will need to resolve. Save resoultion for after comparisons.
      Similarly for the case of originNodeC
        If Vk or Vl is A, then we can join. But if Vk and Vl are not A, then we will need to resolve.
      If we have a join on B and on C, we need to consider if they will conflict
        Conflict would occur if Vi or Vj is equal to Vk or Vl. If so, we can only join on one and should join the more promising value.
        If we do not have conflict, then we can join both.
        Updated chains have the form of [trueValue, originNode, [leftNode0, leftNode1, ... leftNodeN], [rightNode0, rightNode1, ... rightNodeN], avg. promising value]
        Where the idea of sequential left and right nodes plays out as follows
          The Nth most left node would be placed first, so it can be seen to be a stack that is popped off.
          When the left nodes are empty, the origin node is placed
          Then, the rightMost Nodes are treated like a queue, where the pop will be from the front, and the last rightMost Node is then removed
          This forms the chain naturally as below
          leftNodeN-leftNodeN-1-...leftNode0-originNode-rightNode0...rightNodeN-1-rightNodeN
          Before starting then, we should first loop through and form all chains as this format entails, then we can more easily allow for us to access and modify as we see fit
      If we have a join on B or C, and a conflict on the other, we need to first do the join, then calculate the new average value. If we do a join there will still be a conflict.
        We then move to resolution, where the chain with greatest promising value is retained and the other is discarded.
      If wew have a conflict on B and C, we just keep the greatest promising value and remove the others.
      After the end, the non-promising are removed, and the promising remains. This continues until either all chains are independent or only one chain remains, whichever comes first
    '''
    # First phase, put all chains in new form
    newFormatList = []
    for chain in true_chains:
        # This new form allows us to have the truth value, the originNode, the leftNodes and rightNodes as lists, and the promising value
        newFormatList.append([chain[0], chain[1], [chain[2]], [chain[3]], chain[4]])
    # all chains now in new format
    # find matches algorithm stop points
    noMatchingChains = 0
    if len(newFormatList) == 1:
        return newFormatList  # That's the only promising chain
    else:
        # stop if at one chain or if all independent
        for i in range(len(newFormatList)):
            if newFormatList[i][0] == False:
                continue  # Skip false items
            # See if there is a conflict set at chain i
            chainIOrigin = newFormatList[i][1]
            chainILeftList = newFormatList[i][2]
            chainIRightList = newFormatList[i][3]
            # get any chains that may have conflict by searching the rest of the list
            matchingChains = []
            for j in range(len(newFormatList)):
                if i == j or newFormatList[j][0] == False:
                    continue  # Don't compare on the same item or on False items
                else:
                    # Otherwise, we need to catch this item as needed
                    # When we catch the items, we need to compare and contrast the differences
                    # To see if they match, we can just go through and see if there is a match between the chainIOrigin, chainILeftList and chainIRightList
                    if newFormatList[j][1] in chainILeftList or newFormatList[j][1] in chainIRightList:
                        # This means we have a match for the origin node for this chain in the list with the node we're currently resolving
                        if newFormatList[j] not in matchingChains:
                            matchingChains.append(newFormatList[j])
                            allIndependent = False
                    else:
                        # Check the left list current
                        for item in newFormatList[j][2]:
                            if item in chainILeftList or item in chainIRightList or item == chainIOrigin:
                                if newFormatList[j] not in matchingChains:
                                    matchingChains.append(newFormatList[j])
                                    allIndependent = False
                                    # Then do the right
                        for item in newFormatList[j][3]:
                            if item in chainILeftList or item in chainIRightList or item == chainIOrigin:
                                if newFormatList[j] not in matchingChains:
                                    matchingChains.append(newFormatList[j])
                                    allIndependent = False
            if len(matchingChains) == 0:
                continue
            else:
                # for the matching chains are any of them conflict chains
                # conflict chain would have a origin node that is in the IChain's left or right but the conflict chain does not have the origin node in its left or right
                # merge chains have a origin node that is in the IChain's left or right, have the IChain origin node in the left or right, and the origin node is as many down the left or right as this chain's origin
                # and the pattern has to match
                # All of these must be popped from the newFormatList -> all must be removed and put into temporary
                # B-A-C (A is origin, B is left, C is right) -> Current IChain
                # A-C-D (C is origin, A is left, D is right) Merge -> Look for any chains that have an origin node that is in my left or right
                # E-B-D (B is origin, E is left, D is right) Conflict
                # A-J-L (J is origin, A is left, L is right) Conflict, since A has different neighbors
                mergingChains = []
                conflictingChains = []
                for chain in matchingChains:
                    if chain[1] in chainILeftList or chain[1] in chainIRightList:  # If it's got the
                        if chainIOrigin in chain[2] or chainIOrigin in chain[3]:  # If it's got the origin in the left or right
                            mergingChains.append(chain)  # Then it's a merge
                        else:
                            conflictingChains.append(chain)
                    else:
                        conflictingChains.append(chain)
                if len(mergingChains) == 0:
                    # need to find the least promise value among conflicts and the iChain,
                    # that one gets to stay, all others get removed
                    conflictingChains.sort(key=lambda y: y[4], reverse=True)
                    # Attempting change in logic to see result alteration. Resetting logic.
                    if newFormatList[i][4] > conflictingChains[0][4]:
                        # This means that our original was lesser, need to set all of these 0's items to false
                        for chain in conflictingChains:
                            # Go get the index of that chain
                            indexOfThisChain = newFormatList.index(chain)
                            newFormatList[indexOfThisChain][0] = False
                    else:
                        # This means that our original either was greater than our least conflict
                        newFormatList[i][0] = False
                        for k in range(1, len(conflictingChains)):
                            indexOfThisChain = newFormatList.index(conflictingChains[k])
                            newFormatList[indexOfThisChain][0] = False  # Everything but the greatest
                        # we are now done with this cycle
                elif len(mergingChains) == 1:
                    # do the sort, then compare without merging, if better merge, otherwise, render falses
                    if len(conflictingChains) != 0:
                        conflictingChains.sort(key=lambda y: y[4], reverse=True)
                        if ((newFormatList[i][4] + mergingChains[0][4]) / 2.0) > conflictingChains[0][4]:
                            # Merge, then do the set to false thing
                            if chainIOrigin in mergingChains[0][2]:  # on the left
                                # B-A-C Ith chain, origin is A
                                # A-C-D A is in the left, C is in the right, D is one more to the right
                                newFormatList[i][3].extend(mergingChains[0][3])  # Extend the chain
                                newFormatList[i][4] = ((newFormatList[i][4] + mergingChains[0][4]) / 2.0)  # Get the new average
                                # Go false everything in the other lists
                                indexOfTheMergeChain = newFormatList.index(mergingChains[0])
                                newFormatList[indexOfTheMergeChain][0] = False
                                for chain in conflictingChains:
                                    indexOfThisChain = newFormatList.index(chain)
                                    newFormatList[indexOfThisChain][0] = False
                            elif chainIOrigin in mergingChains[0][3]:  # on the right
                                # B-A-C Ith chain, origin is A
                                # D-B-A A is in the right, B is in the left, D is one further left
                                newFormatList[i][3].insert(0, mergingChains[0][3][0])  # Extend the chain
                                newFormatList[i][4] = ((newFormatList[i][4] + mergingChains[0][4]) / 2.0)  # Get the new average
                                # Go false everything in the other lists
                                indexOfTheMergeChain = newFormatList.index(mergingChains[0])
                                newFormatList[indexOfTheMergeChain][0] = False
                                for chain in conflictingChains:
                                    indexOfThisChain = newFormatList.index(chain)
                                    newFormatList[indexOfThisChain][0] = False
                        else:
                            newFormatList[i][0] = False
                            for k in range(1, len(conflictingChains)):
                                indexOfThisChain = newFormatList.index(conflictingChains[k])
                                newFormatList[indexOfThisChain][0] = False  # Everything but the greatest
                            # we are now done with this cycle
                    else:
                        # No conflicting chains, but have a merge chain
                        if chainIOrigin in mergingChains[0][2]:  # on the left
                            newFormatList[i][3].extend(mergingChains[0][3])  # Extend the chain
                            newFormatList[i][4] = ((newFormatList[i][4] + mergingChains[0][4]) / 2.0)  # Get the new average
                            # Go false everything in the other lists
                            indexOfTheMergeChain = newFormatList.index(mergingChains[0])
                            newFormatList[indexOfTheMergeChain][0] = False
                        elif chainIOrigin in mergingChains[0][3]: # on the right
                            newFormatList[i][3].insert(0, mergingChains[0][3][0])  # Extend the chain
                            newFormatList[i][4] = ((newFormatList[i][4] + mergingChains[0][4]) / 2.0)  # Get the new average
                            # Go false everything in the other lists
                            indexOfTheMergeChain = newFormatList.index(mergingChains[0])
                            newFormatList[indexOfTheMergeChain][0] = False
                else:
                    mergingChains.sort(key=lambda y: y[4], reverse=True)
                    # do the sort, then compare without merging, if better merge, otherwise, render falses
                    if len(conflictingChains) != 0:
                        conflictingChains.sort(key=lambda y: y[4], reverse=True)
                        if ((newFormatList[i][4] + mergingChains[0][4]) / 2.0) > conflictingChains[0][4]:
                            # Merge, then do the set to false thing
                            if chainIOrigin in mergingChains[0][2]:  # on the left
                                # B-A-C Ith chain, origin is A
                                # A-C-D A is in the left, C is in the right, D is one more to the right
                                newFormatList[i][3].extend(mergingChains[0][3])  # Extend the chain
                                newFormatList[i][4] = ((newFormatList[i][4] + mergingChains[0][4]) / 2.0)  # Get the new average
                                # Go false everything in the other lists
                                indexOfTheMergeChain = newFormatList.index(mergingChains[0])
                                newFormatList[indexOfTheMergeChain][0] = False
                                for chain in conflictingChains:
                                    indexOfThisChain = newFormatList.index(chain)
                                    newFormatList[indexOfThisChain][0] = False
                            elif chainIOrigin in mergingChains[0][3]:  # on the right
                                # B-A-C Ith chain, origin is A
                                # D-B-A A is in the right, B is in the left, D is one further left
                                newFormatList[i][3].insert(0, mergingChains[0][3][0])  # Extend the chain
                                newFormatList[i][4] = ((newFormatList[i][4] + mergingChains[0][4]) / 2.0)  # Get the new average
                                # Go false everything in the other lists
                                indexOfTheMergeChain = newFormatList.index(mergingChains[0])
                                newFormatList[indexOfTheMergeChain][0] = False
                                for chain in conflictingChains:
                                    indexOfThisChain = newFormatList.index(chain)
                                    newFormatList[indexOfThisChain][0] = False
                        else:
                            newFormatList[i][0] = False
                            for k in range(1, len(conflictingChains)):
                                indexOfThisChain = newFormatList.index(conflictingChains[k])
                                newFormatList[indexOfThisChain][0] = False  # Everything but the greatest
                            # we are now done with this cycle
        newFormatList.sort(key=lambda y:y[0], reverse = True) # Puts in order True to false
        finalList = []
        for chain in newFormatList:
            if chain[0] == True:
                finalList.append(chain)
        finalList.sort(key=lambda y : y[4], reverse = True) # Return the final list with most promising chain first
        return finalList

N = 16 # the number of cities in maine, aka number of nodes

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

# TODO : run the promising sequence function on each row number in the adjacency matrix, appending the return list to a big list of promising chains
def run_full_m( adjacencyMatrix ):
    full_result = []
    true_results = []
    for row in range(len(adjacencyMatrix)):
        promising_r = promising_sequence(adjacencyMatrix, row)
        if promising_r[0]:
            true_results.append(row)
        full_result.append(promising_r)
    return full_result, true_results


full_r, true_results = run_full_m(distance)
# TODO : check to see if the big list has any items whose first item is True
# TODO : If a true was found, remove any items that have a value of False
hadATrueChain = False
if len(true_results) > 0:
    temp = []
    for row in true_results:
        temp.append(full_r[row])
    full_r = temp
    final_set = join_chains(full_r) # Get the final set
    hadATrueChain = True

    # TODO : Come up with a way to compare / join chains join chains is done
    # TODO : If no true was found, just select the item with the largest promising value
else:
    full_r.sort(key=lambda y:y[4], reverse=True) # Get the largest
    # largest_p = full_r[0] # We want this to be the same format as the joined chains though
    # Format is [Boolean, OriginNode, ListOfLeftNodes[], ListOfRightNodes[], promisingValue]
    largest_p = [full_r[0][0], full_r[0][1], [full_r[0][2]], [full_r[0][3]], full_r[0][4]]


# If you have the largest_p or your have the final_set, get the best comparison and run MCMC with limited range based on size
# Need to make sure correct components get placed

# We need to modify simulateSet to use the best chain as the values at the start of the simulation, then not mess with those when you do the random switching
# To do this, best if we pass in the best chain item
chainToPass = []
if hadATrueChain:
    print(final_set) # Print out the final set if you have a few
    chainToPass.extend(final_set) # Get the entire final set
else:
    chainToPass.append(largest_p) # Otherwise, just get the largest amount


def simulateSet(passedChains:list=[], numberOfSimulations:int=10, TVal:int = -1):
    # Moved these to the top
    setOfBestDistances = []
    setOfBestPaths = []
    if len(passedChains) != 0:
        # This is where the modified version goes
        # Need to know areas to not modify based on promising chain currently considering. Want to do this for each of the chains
        for chain in passedChains:
            print("\n")
            print("Current chain consideration")
            print(chain)
            # We'll iterate over each of the passed chains
            currentChainLength = 1+len(chain[2])+len(chain[3]) # Get the length of the chain as an integer. This is how much to add to the 1 to avoid modification
            ITER = 100000 # Set iterations large enough. May want to modify for demo.
            L = np.arange(N) # Makes an arranged array of even spacing of integers
            # Now we want to impose our current chain
            # Start with the left array. Snag each item from the back, swapping it with whatever is needed so it is at the front, moving forward after each
            hasSnaggedOrigin = False
            for index in range(currentChainLength):
                # index is where we currently are pointing
                # want to get the item in the current chains left index that is still there.
                newItem = -1 # Set to negative originally
                if len(chain[2]) != 0:
                    newItem = chain[2].pop() # Pop off the back for the left
                else:
                    if not hasSnaggedOrigin:
                        newItem = chain[1] # get the origin value
                        hasSnaggedOrigin = True
                    else:
                        if len(chain[3]) != 0:
                            newItem = chain[3].pop(0) # Pop off the front for the right
                # now we need to know where that item is in the numpy array
                if(newItem == -1):
                    # Didn't get anything, abort. Index will point to location where we stopped at, i.e. is not included
                    break
                # Otherwise, swap and continue
                indexOfnewItem = np.where(L==newItem) # Go find the index of this item
                # now we need to swap the positions of these two values
                # L[[index, indexOfnewItem]] = L[[indexOfnewItem, index]]
                temp = L[index]
                L[index] = L[indexOfnewItem]
                L[indexOfnewItem] = temp
            # End for loop means we have placed the original values
            if index <= currentChainLength:
                # Means we had to stop early, as something weird must have happened
                currentChainLength = index
                # This puts us back to the earlier stopping point
            # Otherwise, we are greater on index, indicating the non-inclusive aspect mentioned above
            # Now we can loop the simulations
            for j in range(numberOfSimulations):
                d_t = cal_dist(distance, L)
                if(j == 0):
                    best = L
                    best_distance = cal_dist(distance, L)
                else:
                    # check to see if better
                    if d_t < best_distance:
                        best = L
                        best_distance = d_t
                    else:
                        L=best
                print("Modified L and distance : ", L)
                print(cal_dist(distance, L))
                dist_all = []
                # Set the temperature appropriately for each simulation
                if TVal == -1:
                    T = 1000
                else:
                    T = TVal
                # Now for each simulation we do our iterations
                for iteration in range(ITER):
                    # Allowing it to snag to see results
                    a = np.random.randint(1, N-1)
                    d_t = cal_dist(distance, L)
                    dist_all.append(d_t)
                    L_tmp = copy.copy(L)
                    L_tmp[[a, (a + 1)%N]] = L_tmp[[(a + 1)%N, a]] # Set the L_temp at the position and position+1 modulo N to the value at position+1 module N and position (does the swap of the value positions)
                    L_tmp_dst = cal_dist(distance, L_tmp)
                    delta_d = cal_dist(distance, L_tmp) - d_t # Get the distance of the new set up
                    if delta_d < 0 or ( T > 0 and random.random() < math.exp(-1*delta_d/T)): # Make a decision based on either improvement, or based on random selection
                        L = L_tmp
                    if d_t < best_distance:
                        best = L_tmp
                        best_distance = cal_dist(distance, L_tmp)
                    if T > 3:
                        T -= 2
                    else:
                        T = float(T) / (float(iteration)+(1.0*(TVal+1)))
                print("Final L and distance : ", L)
                finalDistance = cal_dist(distance, L)
                print(finalDistance) # final distance
                plt.plot(dist_all)
                setOfBestDistances.append(finalDistance)
                setOfBestPaths.append(L)
            minDist = min(setOfBestDistances)
            bestPath = setOfBestPaths[setOfBestDistances.index(minDist)]
            print("After ", numberOfSimulations, " the best path and distance found below for current chain")
            print(minDist)
            print(bestPath)
    else:
        # Everything below here will need to be indented once, done.
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
            print(finalDistance) # final distance
            plt.plot(dist_all)
            setOfBestDistances.append(finalDistance)
            setOfBestPaths.append(L)
        minDist = min(setOfBestDistances)
        bestPath = setOfBestPaths[setOfBestDistances.index(minDist)]
        print("After ", numberOfSimulations, " the best path and distance found below")
        print(minDist)
        print(bestPath)

def simulateBiggerGroupsOfSets(passedChains:list=[], numberOfSimulations:int = 10):
    # Couple rounds of tests later and there seems to be a discrepancy towards
    # different temperatures. Varying temperature may be more effective in the long run.
    # Seems to be somewhere above 10 and below 10000, which is a range to be sure.
    # Also may be that different temperatures work better for different set ups as well.
    # TList = [0, 1, 10, 100, 1000, 10000, 50000, 100000]
    TList = [100]
    if len(passedChains) == 0:
        for k in range(len(TList)):
            print("Results for T = ", TList[k])
            simulateSet([], 10, TList[k])
            print("End Results for set \n\n")
    else:
        # Use steady temperature of 100
        print("Results for T = 100 and chain passing")
        simulateSet(passedChains, 10, 100)
        print("End of Results for set \n\n")

simulateBiggerGroupsOfSets()
print(chainToPass)
simulateBiggerGroupsOfSets(chainToPass)
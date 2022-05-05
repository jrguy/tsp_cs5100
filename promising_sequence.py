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
import math


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




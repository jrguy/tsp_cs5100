import sys
from processor_json import ProcessorJson
from map import cities, cities2
import TSPAttempt1


def main(argv):
    output = "output/"
    input_loc = "output/"
    tab = 4
    api_url = ""

    len_args = len(sys.argv)
    if len_args > 0:
        if len_args >= 3:
            output = sys.argv[1]
            input_loc = sys.argv[2]
            tab = int(sys.argv[3])
            api_url = sys.argv[4]

    # Create the Processor to input JSON files
    jsonProc = ProcessorJson(output, input_loc, tab)
    # writes the cities json file
    # jsonProc.write_dic(cities, "cities")
    #


    # Some methods to update Json files
    # jsonProc.update_file(cities2, "cities", output)
    #
    # api_result = jsonProc.read_in(api_url, True, "example")
    #
    # print(api_result)

    # Writes the 16-cities file
    # data = jsonProc.write_new_data()
    #
    # jsonProc.write_dic_out(data, "16-cities", output)

    # Read in a Json file and pass to the algo to find the most promising results
    result = jsonProc.read_dic("16-cities")

    print(result)

    adj_mat = jsonProc.make_adjacency_m(result)

    print(adj_mat)

    print("Current Adjacency Matrix Below ")
    for row in range(len(adj_mat)):
        print(adj_mat[row])
    print("\n")

    # run the below to proces the current matrix

    bestFourByRowOfAdjacencyMatrix = TSPAttempt1.findMinimFour(adj_mat)
    print("Best 4 neighbors in adjacency matrix below ")
    for row in bestFourByRowOfAdjacencyMatrix:
        print(row)
    print("\n")

    full_r, true_results = TSPAttempt1.run_full_m(adj_mat)
    hadATrueChain = False
    final_set = []
    largest_p = []
    if len(true_results) > 0:
        temp = []
        for row in true_results:
            temp.append(full_r[row])
        full_r = temp
        final_set = TSPAttempt1.join_chains(full_r) # Get the final set
        hadATrueChain = True
    else:
        full_r.sort(key=lambda y:y[4], reverse=True) # Get the largest
        # largest_p = full_r[0] # We want this to be the same format as the joined chains though
        # Format is [Boolean, OriginNode, ListOfLeftNodes[], ListOfRightNodes[], promisingValue]
        largest_p = [full_r[0][0], full_r[0][1], [full_r[0][2]], [full_r[0][3]], full_r[0][4]]

    chainToPass = []
    if hadATrueChain:
        print(final_set) # Print out the final set if you have a few
        chainToPass.extend(final_set) # Get the entire final set
    else:
        chainToPass.append(largest_p) # Otherwise, just get the largest amount

    TSPAttempt1.simulateBiggerGroupsOfSets()
    print(chainToPass)
    TSPAttempt1.simulateBiggerGroupsOfSets(chainToPass)




if __name__ == "__main__":
    main(sys.argv)

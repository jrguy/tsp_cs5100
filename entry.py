import sys
from processor_json import ProcessorJson
from map import cities, cities2


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

    jsonProc = ProcessorJson(output, input_loc, tab)

    jsonProc.write_dic(cities, "cities")

    result = jsonProc.read_dic("cities")

    print(result)

    # need better update or merge for that data
    jsonProc.update_file(cities2, "cities", output)

    api_result = jsonProc.read_in(api_url, True, "example")

    print(api_result)


if __name__ == "__main__":
    main(sys.argv)

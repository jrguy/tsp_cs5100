import json
import requests
import city_list

class ProcessorJson:

    def __init__(self, output="output/", inputPath="output/", indent=4):
        self.outputPath = output
        self.inputPath = inputPath
        self.indent = indent

    def write_dic(self, data, file_name):
        json_object = json.dumps(data, indent=self.indent)

        output_file = open(self.outputPath + file_name + ".json", "w")
        output_file.write(json_object)
        output_file.close()

    def write_dic_out(self, data, file_name, output):
        json_object = json.dumps(data, indent=self.indent)

        output_file = open(output + file_name + ".json", "w")
        output_file.write(json_object)
        output_file.close()

    def update_file(self, data, file_name, dir_loc):
        with open(dir_loc + file_name + ".json", "r+") as file:
            file_data = json.load(file)

        # file_data["emp_details"].append(new_data)
        # file.seek(0)

        new_data = [file_data, data]

        with open(dir_loc + file_name + ".json", 'w') as file:
            json.dump(new_data, file, indent=self.indent)

    def read_dic(self, file_name):
        f = open(self.inputPath + file_name + ".json")
        data = json.load(f)
        f.close()

        return data

    def read_in(self, url, write_bool, file_name="example"):
        obj = requests.get(url).json()

        if write_bool:
            self.write_dic(obj, file_name)
        else:
            return obj

    def write_new_data(self):
        cities = city_list.cities
        distances = city_list.distances
        final = {}
        i = 0
        for city in cities:
            final[city] = {}
            final[city]['start'] = {}
            final[city]['end'] = {}
            dist_i = 0
            for distance in distances:
                if dist_i != i:
                    final[city]['start'][cities[dist_i]] = distance
                    final[city]['end'][cities[dist_i]] = distance
                else:
                    final[city]['start'][cities[dist_i]] = 0
                    final[city]['end'][cities[dist_i]] = 0
                dist_i += 1
            i += 1

        return final

    def make_adjacency_m(self, data):
        adj_m = []
        key_list = {}
        list_ind = 0
        index = 0

        for key, value in data.items():
            adj_m.insert(list_ind, [])
            if key not in key_list:
                key_list[key] = index
                index += 1
            for sub_key, sub_val in data[key]['start'].items():
                if sub_key not in key_list:
                    key_list[sub_key] = index
                    index += 1
            for sub_key, sub_val in data[key]['end'].items():
                if sub_key not in key_list:
                    key_list[sub_key] = index
                    index += 1
            list_ind += 1

        list_ind = 0
        for key, value in data.items():
            cur_index = 0
            for found_k in key_list.items():
                adj_m[list_ind].insert(cur_index, 0)
                cur_index += 1
            list_ind += 1

        list_ind = 0
        for key, value in data.items():
            for sub_key, sub_val in data[key]['start'].items():
                cur_index = key_list[sub_key]
                adj_m[list_ind][cur_index] = sub_val
            # for sub_key, sub_val in data[key]['end'].items():
            #     cur_index = key_list[sub_key]
            #     adj_m[cur_index][list_ind] = sub_val
            list_ind += 1
        return adj_m

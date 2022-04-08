import json
import requests

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

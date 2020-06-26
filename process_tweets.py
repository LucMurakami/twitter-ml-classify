""" Processes json objects returned to the data folder to csv """

import os, json

cur_folder = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(cur_folder, "data/")
json_files = [file for file in os.listdir(data_dir) if file.endswith(".json")]

for index, each_json in enumerate(json_files):
    with open(os.path.join(data_dir, each_json)) as json_file:
        tweets = json.load(json_file)

        text = ""
        name = each_json.split(sep=".")[0]
        file_version = '1'
        file_exists = True

        while file_exists:
            try:
                file = open("./data/{}_{}.csv".format(name, file_version), "x")
            except IOError:
                file_version = str(int(file_version)+1)
            else:
                with file:
                    file_exists = False
                    for tweet in tweets:
                        file.write('"{}",\n'.format(tweet["full_text"].replace("\n", " ")))


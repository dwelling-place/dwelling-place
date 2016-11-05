import json


def save_json(data, path):
    with open(path, 'w') as outfile:
        json.dump(list(data), outfile, indent=4)

    return path

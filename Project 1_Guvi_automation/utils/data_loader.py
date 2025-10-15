import json
import os

def load_test_data(file_name): # Loads test data from a JSON file located in the same directory
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    # Dynamically constructs the absolute path to the JSON file

    with open(file_path, "r") as f:
    # Opens the file in read mode

        return json.load(f)
        #  Parses the JSON content and returns it as a Python dictionary.
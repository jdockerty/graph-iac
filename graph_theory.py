import networkx as nx
import matplotlib as plt
import json
from pathlib import Path


class graph_structure:
    path_to_file = ""
    current_graph = None

    def __init__(self):
        self.current_graph = nx.Graph()

    def get_json_to_dict(self):
        file_path = Path(self.path_to_file)
        with file_path.open(mode='r') as my_file:
            JSON_to_dict = dict(json.load(my_file))
            return JSON_to_dict

    def set_filepath(self, filepath):
        self.path_to_file = filepath

    def get_resources(self):
        json_as_dict = self.get_json_to_dict()
        return json_as_dict['Resources'].keys()

    def add_nodes(self):
        self.current_graph.add_node(self.get_resources())


test = graph_structure()
test.set_filepath(r'C:\Users\Jack\PycharmProjects\GraphTheoryToIaC\Files_To_Read\template.json')
print(test.get_resources())

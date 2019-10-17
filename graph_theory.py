import networkx as nx
import matplotlib as plt
import json
from pathlib import Path
from nested_lookup import get_all_keys, nested_lookup


class graph_structure:
    path_to_file = ""
    current_graph = None
    node_dependencies = {}

    def __init__(self):
        self.current_graph = nx.Graph()

    def get_json_to_dict(self):
        file_path = Path(self.path_to_file)
        with file_path.open(mode='r') as my_file:
            full_json_to_dict = dict(json.load(my_file))
            return full_json_to_dict

    def set_filepath(self, filepath):
        self.path_to_file = filepath

    def get_resources_count(self):
        resources_json_as_dict = self.get_json_to_dict()
        return resources_json_as_dict['Resources'].keys()

    def add_nodes(self):
        self.current_graph.add_node(self.get_resources_count())

    def map_edges_to_nodes(self):
        current_JSON = self.get_json_to_dict()['Resources'] # Pulls the full JSON, BUT ONLY RESOURCES KEY AND AFTER
        print(current_JSON)
        counter = 0
        resources_list = list(current_JSON)
        print(resources_list)
        print("\n\n\n ----DICT----")

        for key in list(current_JSON.items()):
            sub_dict = key[1]
            print("Full Dict: ",sub_dict)
            print("Keys only: ", get_all_keys(sub_dict))
            print("\n")
            try:

                if 'Ref' in get_all_keys(sub_dict):
                    self.node_dependencies[resources_list[counter]] = nested_lookup('Ref', sub_dict)
                    print(self.node_dependencies)
                elif 'InstanceId' in get_all_keys(sub_dict):
                    self.node_dependencies[resources_list[counter]] = nested_lookup('InstanceId', sub_dict)
                    print(self.node_dependencies)
                    print("Int")
                elif 'DependsOn' in get_all_keys(sub_dict):
                    self.node_dependencies[resources_list[counter]] = nested_lookup('DependsOn', sub_dict)
                    print(self.node_dependencies)
                    print("Depends")

                # IF SUCCESSFUL THEN ADD THAT VALUE INTO THE DEPENDENCY
                counter += 1
            except KeyError:
                continue

test = graph_structure()
test.set_filepath(r'C:\Users\Jack\PycharmProjects\GraphTheoryToIaC\Files_To_Read\template.json')
test.map_edges_to_nodes()


# IDEA - TRAVERSE RESOURCES SUB-DICT AND READ FOR DependsOn/Other dependencies, if exists then can add to dict. Map edges
# from that generated dict.

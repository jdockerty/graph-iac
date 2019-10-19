import networkx as nx
import matplotlib.pyplot as plt
import json
import ruamel.yaml
from pathlib import Path
from nested_lookup import get_all_keys, nested_lookup
from collections.abc import Iterable


class GraphStructure:
    path_to_file = ""
    current_graph = None
    node_dependencies = {}
    file_format = ""

    def __init__(self, directed=True):
        """
        Constructor for initial class, creates an empty graph.
        """
        if directed:
            self.current_graph = nx.DiGraph()
        if not directed:
            self.current_graph = nx.Graph()

    def get_json_to_dict(self):
        """
        Uses the file-path provided in the set_filepath method to read the JSON file and convert it to a dictionary.
        This is done so that the data can be accessed and manipulated to build the graph.

        :return dict:
        """
        filepath = Path(self.path_to_file)
        with filepath.open(mode='r') as my_file:
            full_json_to_dict = dict(json.load(my_file))
            return full_json_to_dict

    def get_file_to_dict(self):
        self.check_file_format()

        if self.file_format == 'YAML':
            return self.is_yaml_format()
        elif self.file_format == 'JSON':
            return self.get_json_to_dict()
        elif self.file_format == 'TERRAFORM':
            pass

    def check_file_format(self):
        try:
            if '.yml' in self.path_to_file:
                self.file_format = "YAML"

            elif '.json' in self.path_to_file:
                self.file_format = "JSON"

            elif '.tf' in self.path_to_file:
                self.file_format = "TERRAFORM"

        except FileNotFoundError:
            raise FileNotFoundError("You must set the file path using the set_filepath method "
                                    "before this is used.")

    def is_yaml_format(self):
        if 'YAML' in self.file_format:
            yaml = ruamel.yaml.YAML(typ='safe')
            filepath = Path(self.path_to_file)
            with filepath.open(mode='r') as yml_file:
                yml_data = yaml.load(yml_file)
                return yml_data
            # Cannot seem to resolve !Ref short form, although replacing this to
            # full function name seems to work for now.

    def set_filepath(self, filepath):
        """
        Method used for setting the filepath to the JSON file containing the Cloudformation template.

        :param filepath:
        :return:
        """
        self.path_to_file = filepath
        return True

    def get_resources_count(self):
        """
        Used for retrieving the number of keys in the sub-dict of the Resources key as an integer, this is directly
        linked to the number of nodes required to construct the graph.

        :return integer:
        """
        resources_json_as_dict = self.get_file_to_dict()
        return len(resources_json_as_dict['Resources'].keys())

    def get_nodes(self):
        """
        Retrieves the keys in the sub-dict for Resources key itself. These are the nodes required for the graph.

        :return list:
        """
        resources_json_as_dict = self.get_file_to_dict()
        return list(resources_json_as_dict['Resources'].keys())

    def add_nodes(self):
        """
        This adds the number of nodes generated from the get_resources_count method onto the current graph.

        :return:
        """
        self.current_graph.add_nodes_from(self.get_nodes())

    def add_edges(self):

        """
        For each k,v in the tuple (node, dependent_node)
            if v is Iterable:
                for v_2 in v:

            else:
                add_edge(k,v)


        """

        tuple_of_edges = tuple(self.node_dependencies.items())
        print(tuple_of_edges)
        for node, node_dependencies in tuple_of_edges:
            if isinstance(node_dependencies, Iterable):
                for singular_node in node_dependencies:
                    self.current_graph.add_edge(node,singular_node)

    def remove_nested_list_dependencies(self, nested_list):
        """
        Utility function for flattening a list, sometimes dependencies will return a nested/junk list which makes it
        very troublesome to map to a particular key for showing dependencies. This method ensures that the list is as
        you would expect and then can be mapped accordingly.

        :param nested_list:
        :return list:
        """
        flat_list = []

        for item in nested_list:
            if isinstance(item, Iterable) and not isinstance(item, str):
                flat_list.extend(self.remove_nested_list_dependencies(item))
            else:
                flat_list.append(item)
        return flat_list


    def set_node_dependencies(self):
        """
        Builds the nodes arc's by mapping the other nodes that they are dependant on. This is done through searching for
        key words: DependsOn, InstanceId, and Ref. The keywords are used to show that a particular resource is linked
        in someway to another, so this should be shown on the graph.

        :return:
        """
        current_json = self.get_file_to_dict()['Resources'] # Pulls the full JSON, BUT ONLY RESOURCES KEY AND AFTER
        counter = 0
        resources_list = list(current_json)


        for key in list(current_json.items()):
            sub_dict = key[1]
            try:

                if 'Ref' in get_all_keys(sub_dict):
                    self.node_dependencies[resources_list[counter]] = nested_lookup('Ref', sub_dict)

                elif 'InstanceId' in get_all_keys(sub_dict):
                    self.node_dependencies[resources_list[counter]] = nested_lookup('InstanceId', sub_dict)
                elif 'DependsOn' in get_all_keys(sub_dict):
                    #  This part could be replicated into other statements if they present
                    #  the nested list issue in the future.
                    dependencies_list = nested_lookup('DependsOn', sub_dict)
                    flat_list = self.remove_nested_list_dependencies(dependencies_list)
                    self.node_dependencies[resources_list[counter]] = flat_list
                counter += 1
            except KeyError:
                continue

    def draw_and_show(self, labels_on=True):
        nx.draw(self.current_graph, with_labels=labels_on)
        plt.draw()
        plt.waitforbuttonpress()
        plt.close()
        return True


# IDEA - TRAVERSE RESOURCES SUB-DICT AND READ FOR DependsOn/Other dependencies, if exists then can add to dict. Map edges
# from that generated dict.

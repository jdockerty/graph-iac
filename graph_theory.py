import networkx as nx
import matplotlib.pyplot as plt
import json
import ruamel.yaml
import random
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
        Constructor for initial class, creates an empty graph. The user can specify whether they want a directed or
        undirected graph based on changing the directed default parameter.
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
        """
        Used for running the relevant method based on the file_format variable, this has to be populated first, hence
        why the check_file_format() is called beforehand - this covers the user needing to do it.

        :return:
        """
        self.check_file_format()

        if self.file_format == 'YAML':
            return self.is_yaml_format()
        elif self.file_format == 'JSON':
            return self.get_json_to_dict()
        elif self.file_format == 'TERRAFORM':
            pass
            # Extension idea, although parsing HCL to JSON/usable format seems incredibly time consuming. Something
            # to look into with extra time.

    def check_file_format(self):
        """
        Sets the file_format variable based on what the filepath contains: .yml, .json, and .tf.

        :return:
        """
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

    def get_current_nodes(self):
        """
        Utility function to return a list of nodes on the current graph.

        :return:
        """
        return self.current_graph.nodes

    def get_current_edges(self):
        """
        Utility function to return tuple pairs of connecting nodes.

        :return:
        """
        return self.current_graph.edges

    def set_edge_weights(self, random_input=False):
        for node_one, node_two in self.get_current_edges():
            if random_input:
                random_weight = random.randint(1, 25)
                self.current_graph.add_edge(node_one, node_two, weight=random_weight)
                print("({}, {}) edge weight set to: {} ".format(node_one, node_two, random_weight))
            else:
                edge_weight = int(input("Set the weight for ({}, {}) ".format(node_one, node_two)))
                self.current_graph.add_edge(node_one, node_two, weight=edge_weight)

    def set_edge_capacities(self, random_input=False):
        """
        Allows a user to manually set the capacity of each edge for a tuple pair that is returned in the form of (u, v).
        A helpful aid to this is outputting the graph beforehand, so that it is viewable and the edges are known.

        The random_input parameter serves as a mechanism to quickly set a capacity value of between 1 and 25 for all
        edges on the graph, this is mainly for speed/testing purposes.

        :param random_input:
        :return:
        """
        for node_one, node_two in self.get_current_edges():
            if random_input:
                random_capacity = random.randint(1, 25)
                self.current_graph.add_edge(node_one, node_two, capacity=random_capacity)
                print("({}, {}) edge capacity set to: {} ".format(node_one, node_two, random_capacity))
            else:
                capacity_val = int(input("Set the capacity for ({}, {}) ".format(node_one, node_two)))
                self.current_graph.add_edge(node_one, node_two, capacity=capacity_val)

    def is_yaml_format(self):
        """
        Method which checks whether the filepath provided to the template contains .yml, which implies that the file
        itself is a YAML file, therefore it needs to be converted into a dictionary to be worked with.

        :return:
        """
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
        This maps the edges between nodes based on their dependencies. This is achieved by pulling a set of dict_keys
        by way of the .items() on the node_dependencies dictionary, a tuple pair is returned and then iterates over
        it in the appropriate format (node, node_dependencies), if the 'node_depedencies' variable is an iterable object
        (list etc.) it will then iterate into that and map the particular node dependency to the initial node, this is
        the outer-tuple element.

        :return:
        """

        for node, node_dependencies in self.node_dependencies.items():
            if isinstance(node_dependencies, Iterable):
                for singular_node in node_dependencies:
                    self.current_graph.add_edge(node, singular_node)

    def get_sub_graph_from_node(self, specified_node):
        """
        Builds a sub-graph based on a specified node from the user. This is useful in larger graphs when a smaller
        section may be required, displaying only the smaller subsequent graph that is produced from a node and the
        edges that it has connecting to other nodes.

        :param specified_node:
        :return:
        """

        node_adj = self.current_graph.adj[specified_node].keys()
        all_nodes_sub_graph = list(node_adj)
        all_nodes_sub_graph.append(specified_node)
        sub_graph = self.current_graph.subgraph(all_nodes_sub_graph)
        return sub_graph.copy()

    def add_all_edge_weights(self, edge_weights):
        """
        Adds edge weights based on a user value, currently this adds a weight to every edge and cannot be configured
        to specific (u, v) pairs. This functions in a similar manner to adding nodes, with the exception of adding the
        weight parameter

        :param edge_weights:
        :return:
        """
        for node, node_dependencies in self.node_dependencies.items():
            if isinstance(node_dependencies, Iterable):
                for singular_node in node_dependencies:
                    self.current_graph.add_edge(node, singular_node, weight=edge_weights)

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

    def get_flow_max(self, source_node, sink_node):
        """
        Return the maximum flow between a source and sink node, the capacities of the edges must be set on the graph
        before this will function.

        :param source_node:
        :param sink_node:
        :return:
        """

        return nx.maximum_flow(self.current_graph, source_node, sink_node)

    def get_shortest_aug_path(self, source_node, sink_node):
        """
        Returns a residual network after using the shortest augmented path algorithm.

        :param source_node:
        :param sink_node:
        :return:
        """
        residual = nx.algorithms.flow.shortest_augmenting_path(self.current_graph, source_node, sink_node)
        return residual

    def get_paths_between_nodes(self, source_node, target_node, only_shortest=False):
        """
        Returns a list of possible paths between the source and target node on the graph. Optionally, only the shortest
        path can be returned, in this case you must set the only_shortest to be True.

        :param source_node:
        :param target_node:
        :param only_shortest:
        :return:
        """
        paths = []
        for path in nx.all_simple_paths(self.current_graph, source_node, target_node):
                paths.append(path)

        if only_shortest:
            index = 0
            index_to_path_len = {}
            for path in paths:
                index_to_path_len[index] = len(path)
                index += 1
            return paths[min(index_to_path_len, key=index_to_path_len.get)]

        return paths

    def full_build_graph(self, filepath):
        """
        Utility function that circumvents having to call each individual method in the correct order, only a
        filepath is specified and the rest is handled.

        :param filepath:
        :return:
        """
        self.set_filepath(filepath)
        self.add_nodes()
        self.set_node_dependencies()
        self.add_edges()
        return True

    def full_build_graph_with_weights(self, filepath):
        """
        Similar usage as full_build_graph except this includes adding weighted edges between nodes.

        :param filepath:
        :return:
        """
        self.set_filepath(filepath)
        self.add_nodes()
        self.set_node_dependencies()
        self.add_edges()
        self.set_edge_weights()
        return True

    def full_build_graph_with_random_weights(self, filepath):
        """
        Similar usage as full_build_graph_with_weights except this includes adds random weights, mainly for testing.

        :param filepath:
        :return:
        """
        self.set_filepath(filepath)
        self.add_nodes()
        self.set_node_dependencies()
        self.add_edges()
        self.set_edge_weights(random_input=True)
        return True

    def save_graph_output(self, output_filename, with_edge_labels=False):
        """
        Save the drawn graph as a .png image, with the user providing the filename. Returns True if this was successful.

        :param output_filename:
        :param with_edge_labels:
        :return:
        """
        if with_edge_labels:
            nx.draw_planar(self.current_graph, with_labels=True)
            nx.draw_networkx_edge_labels(self.current_graph, pos=nx.planar_layout(self.current_graph))
            plt.savefig("Saved_Graphs/{}.png".format(output_filename), format="PNG")
        else:
            nx.draw_planar(self.current_graph, with_labels=True)
            plt.savefig("Saved_Graphs/{}.png".format(output_filename), format="PNG")
        return True

    def set_node_dependencies(self):
        """
        Builds the nodes edges by mapping the other nodes that they are dependant on. This is done through searching for
        key words: DependsOn, InstanceId, and Ref. The keywords are used to show that a particular resource is linked
        in someway to another, so this should be shown on the graph.

        :return:
        """
        def map_dependencies(dependency_tag):
            dependencies_list = nested_lookup(dependency_tag, sub_dict)
            flat_list = self.remove_nested_list_dependencies(dependencies_list)
            self.node_dependencies[resources_list[counter]] = flat_list
            return True

        current_json = self.get_file_to_dict()['Resources'] # Pulls the full JSON, BUT ONLY RESOURCES KEY AND AFTER
        counter = 0
        resources_list = list(current_json)

        for key in list(current_json.items()):
            sub_dict = key[1]
            try:

                if 'Ref' in get_all_keys(sub_dict):
                    # dependencies_list = nested_lookup('Ref', sub_dict)
                    # flat_list = self.remove_nested_list_dependencies(dependencies_list)
                    # self.node_dependencies[resources_list[counter]] = flat_list
                    map_dependencies('Ref')
                elif 'InstanceId' in get_all_keys(sub_dict):
                    # dependencies_list = nested_lookup('InstanceId', sub_dict)
                    # flat_list = self.remove_nested_list_dependencies(dependencies_list)
                    # self.node_dependencies[resources_list[counter]] = flat_list
                    map_dependencies('InstanceId')
                elif 'DependsOn' in get_all_keys(sub_dict):
                    #  This part could be replicated into other statements if they present
                    #  the nested list issue in the future.
                    # dependencies_list = nested_lookup('DependsOn', sub_dict)
                    # flat_list = self.remove_nested_list_dependencies(dependencies_list)
                    # self.node_dependencies[resources_list[counter]] = flat_list
                    map_dependencies('DependsOn')
                counter += 1
            except KeyError:
                continue

    def draw_and_show(self, labels_on=True, planar_layout=True):
        """
        Draws the graph and then displays it in an interactive window with node labels turned on, pressing any key
        or clicking inside of the window will close the window. You can move the window without it closing.

        :param labels_on:
        :param planar_layout:
        :return:
        """
        if planar_layout:
            nx.draw_planar(self.current_graph, with_labels=labels_on)
            plt.waitforbuttonpress()
        else:
            nx.draw_spring(self.current_graph, with_labels=labels_on)
            plt.waitforbuttonpress()
        return True

    def draw_and_show_with_edge_labels(self):
        """
        Draws the graph and displays it with node/edge labels displays. This is somewhat experimental and can be buggy
        dependent on the number of nodes and how edge labels are displayed.

        :return:
        """
        nx.draw_spring(self.current_graph, with_labels=True)
        nx.draw_networkx_edge_labels(self.current_graph, pos=nx.spring_layout(self.current_graph))
        plt.waitforbuttonpress()
        return True

    def draw_sub_graph(self, origin_node):
        """
        Draws and displays the sub-graph, typically a tree, that is created from the original node. This is useful in
        very large graphs to display a smaller subset from a particular node.

        :param origin_node:
        :return:
        """
        sub_graph = self.get_sub_graph_from_node(origin_node)
        nx.draw_spring(sub_graph, with_labels=True)
        plt.show()
        return True

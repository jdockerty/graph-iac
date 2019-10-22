from graph_theory import GraphStructure
import networkx as nx
test = GraphStructure()

test.full_build_graph_with_random_weights(r'C:\Users\Jack\PycharmProjects\GraphTheoryToIaC\Files_To_Read\template_two.json')
test.save_graph_output('setting_weights',with_edge_labels=True)
"""
Reference for networkx package.

Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, 
“Exploring network structure, dynamics, and function using NetworkX”, 
in Proceedings of the 7th Python in Science Conference (SciPy2008), 
Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008

"""

from graph_theory import GraphStructure
import networkx as nx
import matplotlib.pyplot as plt
test = GraphStructure()
test.set_filepath(r'C:\Users\Jack\PycharmProjects\GraphTheoryToIaC\Files_To_Read\template.json')
test.add_nodes()
test.set_node_dependencies()
print(test.node_dependencies)
print(test.current_graph.nodes)
nx.draw(test.current_graph, with_labels=True)
plt.show()

"""
Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, 
“Exploring network structure, dynamics, and function using NetworkX”, 
in Proceedings of the 7th Python in Science Conference (SciPy2008), 
Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008
"""

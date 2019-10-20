from graph_theory import GraphStructure

test = GraphStructure()

test.full_build_graph_with_weights(r'C:\Users\Jack\PycharmProjects\GraphTheoryToIaC\Files_To_Read\template.yml', 3)
test.draw_and_show_with_edge_labels()


"""
Reference for networkx package.

Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, 
“Exploring network structure, dynamics, and function using NetworkX”, 
in Proceedings of the 7th Python in Science Conference (SciPy2008), 
Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008


Let you choose between an undirected and directed graph, also change how it handles the file path maybe and 
try get it to handle YAML format too

"""

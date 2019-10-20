from graph_theory import GraphStructure

test = GraphStructure()

test.full_build_graph_with_weights(r'C:\Users\Jack\PycharmProjects\GraphTheoryToIaC\Files_To_Read\template.yml', 3)
test.save_graph_output('edge_labels_included_no')


"""
Reference for networkx package.

Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, 
“Exploring network structure, dynamics, and function using NetworkX”, 
in Proceedings of the 7th Python in Science Conference (SciPy2008), 
Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008

"""

from graph_theory import GraphStructure

test = GraphStructure()

test.full_build_graph(r'C:\Users\Jack\PycharmProjects\GraphTheoryToIaC\Files_To_Read\template_three.json')
test.get_paths_between_nodes(source_node='ELBMain', target_node='Glacier',only_shortest=True)

"""
Reference for networkx package.

Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, 
“Exploring network structure, dynamics, and function using NetworkX”, 
in Proceedings of the 7th Python in Science Conference (SciPy2008), 
Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008

"""

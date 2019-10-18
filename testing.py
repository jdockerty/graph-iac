from graph_theory import GraphStructure

test = GraphStructure()
test.set_filepath(r'C:\Users\Jack\PycharmProjects\GraphTheoryToIaC\Files_To_Read\template.json')
print(test.get_resources_count())
test.set_node_dependencies()

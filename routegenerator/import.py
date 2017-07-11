import ast
import networkx as nx

def prepare_graph_from_import(string_input):
    graph = nx.Graph()
    string_input = string_input.split("\n")
    flag = False
    for line in string_input:
        line = line.strip('(')
        line = line.strip(')')
        if(flag == False):
            if(line == "|"):
                flag = True
            else:
                elem = line.split(", ")
                node_id = int(elem[0])
                temp_dict_str = elem[1] + ", " + elem[2]
                temp_dict = ast.literal_eval(temp_dict_str)
                graph.add_node(node_id,temp_dict)
        elif(flag == True):
            elem = line.split("{")
            node_id = elem[0].split(",")

            if(node_id[0] != "" and node_id != ""):
                node_id_1 = int(node_id[0])
                node_id_2 = int(node_id[1])

                temp_dict_str = "{" + elem[1]
                temp_dict = ast.literal_eval(temp_dict_str)
                graph.add_edge(node_id_1,node_id_2,temp_dict)

    return graph

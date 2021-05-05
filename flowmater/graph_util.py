"""
******************************
process graph files
******************************
"""

import copy
import networkx as nx
import matplotlib.pyplot as plt


#draw graph
def draw_graph(g):
    pos = nx.spring_layout(g,k=0.2)
    nx.draw_networkx_labels(g, pos, labels =  nx.get_node_attributes(g,'label'))
    plt.figure(1,figsize=(120,120)) 
    nx.draw(g, pos)
    plt.show()
    


def make_simplifierd_graphs(g_list):
    simplified_graph_list=[]
    for g in g_list:
        temp_g=copy.deepcopy(g)

        for node in temp_g.nodes:
            node_dict=temp_g.nodes[node]
            node_dict.pop("x")
            node_dict.pop("y")    
            node_dict.pop("value")        
        
        rename_dict={node:temp_g.nodes[node]["label"] for node in temp_g.nodes}
        temp_g=nx.relabel_nodes(temp_g, rename_dict)
        simplified_graph_list.append(temp_g)
    return simplified_graph_list

def categorize_graphs(g_list):
    simplified_graph_list=make_simplifierd_graphs(g_list)

    #compare grapghs by enumerating the graph nodes
    num_graphs=len(simplified_graph_list)
    graph_category=list(range(num_graphs))


    graph_set_list=[sorted(list(set(g))) for g in simplified_graph_list]
    graph_set_list=["".join(str(i)) for i in graph_set_list]

    graph_name_dict={v:num for num,v in enumerate(set(graph_set_list))}

    #set graph numbers
    graph_type_list=[graph_name_dict[gr] for gr in graph_set_list]
    return {k:v for k,v in zip(range(len(g_list)),graph_type_list)}
    


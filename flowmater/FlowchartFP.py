import copy

#calculate fingerprint of flowchart
class FlowchartFP:
    def __init__(self,g_list):

        #analyze graph list and set node list
        self.all_node_val_list=[]
        for g in g_list:
            self.all_node_val_list.extend(analyze_node_connections(g))
        self.all_node_val_list=list(set(self.all_node_val_list))

        self.template_dict={i:0 for i in range(len(self.all_node_val_list))}
        self.v_to_i={v:i for i,v in enumerate(self.all_node_val_list)}
        self.i_to_v={i:v for i,v in enumerate(self.all_node_val_list)}

    def __call__(self,g):
        node_val_list=analyze_node_connections(g)
        found_fp=copy.copy(self.template_dict)

        for val in node_val_list:
            found_fp[self.v_to_i[val]]=1

        return list(found_fp.values())


#analyze node vals in the flowchart
def analyze_node_connections(g):
    """
    g: networkX object of florchart
    return: list of characteristic node info.
    """
    node_val_list=[]

    for node in g.nodes:
        node_val=g.nodes[node]["label"]
        neighbor_val_list=[]
        for neighbor_node in (g.to_undirected().neighbors(node)):
            neighbor_val_list.append(g.nodes[neighbor_node]["label"])


        neighbor_val_list=sorted(neighbor_val_list)
        node_val+="<-->"+"--".join(neighbor_val_list)


        node_val_list.append(node_val)
    return node_val_list
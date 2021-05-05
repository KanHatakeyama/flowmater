import re
import networkx as nx
from rdkit import Chem
import pandas as pd
import copy
from .graphml_util import load_graphml


#experiment data class, which loads graphml and corresponding xlsx files
class ExperimentData:
    def __init__(self,path):
        self.path=path
        self._initialize()
        
    def _initialize(self):
        #load graphml files as a networkX object, g
        self.g=load_graphml(self.path)
        
        """
        process g
        the graph consists of parent and son nodes.
        parent node list are extracted.
        info of son nodes is added to the parent nodes
        """
        self.g,self.parent_node_list=process_graph(self.g)

        #extract variables in the graphs (e.g., chemicals, number, ...)
        self.experiment_format=make_base_dict(self.g,self.parent_node_list)
        
        #load variables from the corresponding xlsx file
        self.experiment=load_xlsx_of_graph(self.g,self.parent_node_list,self.path,self.experiment_format)


#util funcs

def load_xlsx_of_graph(g,parent_node_list,path,experiment_dict):
    #load recorded data in xlsx
    result_df=pd.read_excel(path.replace(".graphml",".xlsx"),sheet_name="prop")

    #variable list
    variable_name_list=list(result_df.columns)

    #search param keys for the variables
    var_to_key_dict={}
    for name in variable_name_list:
        for k,v in experiment_dict.items():
            if "{"+name+"}"==v:
                var_to_key_dict[v]=k
                break

    #make full database as dict
    database_as_dict={}
    for i in range(result_df.shape[0]):
        temp_dict=copy.deepcopy(experiment_dict)
        
        for k,v in var_to_key_dict.items():
            temp_dict[v]=result_df[k.replace("{","").replace("}","")][i]
        database_as_dict[path.replace(".graphml","")+"_"+str(i)]=temp_dict
        
    return database_as_dict


#extract parent node_list
def get_parent_node_list(g):
    node_list=list(g.nodes)
    parent_node_list=[]
    for content in node_list:
        if re.match('n\d+$', content) is None:
            continue
        try:
            g.nodes[content]["label"]
        except:
            continue
        parent_node_list.append(content)

    return parent_node_list

#add node vals to the parent nodes
def add_node_val(parent_node,g):
    i=0
    val_list=[]
    while True:
        try:
            son_node=parent_node+"::n"+str(i)
            label=g.nodes[son_node]["label"]
        except:
            break

        val_list.append(label)
        i+=1
        
    g.nodes[parent_node]["value"]=sorted(val_list)

#auto process
def process_graph(g):
    parent_node_list=get_parent_node_list(g)    

    for parent_node in parent_node_list:
        #add node values
        add_node_val(parent_node,g)

        #add proc info
        try:
            label=g.nodes[parent_node]["label"]
        except:
            pass

        if label.find("Proc")>=0 or label.find("Measure")>=0:
            new_label=label

            for v in g.nodes[parent_node]["value"]:

                #skip time
                if re.match("^([01][0-9]|2[0-3]):[0-5][0-9]$", v):
                    continue

                #skip memo
                if re.match("memo:.*$", v):
                    continue

                #skip number
                if re.match("\d+$", v):
                    continue
                #skip user variables
                if re.match('{.*}$', v):
                    continue
                new_label+=", "+v

            g.nodes[parent_node]["label"]=new_label

    #delete isolated nodes
    g.remove_nodes_from(list(nx.isolates(g)))
    
    return g,parent_node_list


def make_base_dict(g,parent_node_list):
    experiment_dict={}

    for parent_node in parent_node_list:
        label=g.nodes[parent_node]["label"]
        val_list=g.nodes[parent_node]["value"]

        #load chemicals
        if label.find("Chemical_")>=0:

            #find smiles in values
            smiles_count=0
            for v in val_list:
                m = Chem.MolFromSmiles(v)
                if m is not None:
                    experiment_dict[label+"_SMILES"]=v
                    smiles_count+=1

            #if smiles_count!=1:
            #    print("caution! too many or few smiles! ", val_list)

        #load numberics or user variables
        for val in val_list:
            #number
            if re.match('\d+$', val):
                experiment_dict[label]=float(val)

            #user val
            if re.match('{.*}$', val):
                experiment_dict[label]=val
    return experiment_dict


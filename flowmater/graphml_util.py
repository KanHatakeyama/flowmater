"""
******************************
process graphml files
******************************
"""

import networkx as nx
import os

temp_path="temp.graphml"

def preprocess_graphml(path):
    #modify graphml
    with open(path, encoding="utf-8") as f:
        data_lines = f.read()

    data_lines = data_lines.replace("GenericNode", "ShapeNode")
    data_lines = data_lines.replace("<y:GroupNode>", "")
    data_lines = data_lines.replace("</y:GroupNode>", "")
    data_lines = data_lines.replace("ProxyAutoBoundsNode", "ShapeNode")
    data_lines = data_lines.replace("""<y:Realizers active="0">""", "")
    data_lines = data_lines.replace("</y:Realizers>", "")


    with open(temp_path, mode="w", encoding="utf-8") as f:
        f.write(data_lines)

def load_graphml(path):
    preprocess_graphml(path)    
    g=nx.read_graphml(temp_path)    
    os.remove(temp_path)
    return g

import glob
from .ExperimentData import ExperimentData
from .graph_util import categorize_graphs

from rdkit import RDLogger             
RDLogger.DisableLog('rdApp.*')   

class ExperimentManager:
    def __init__(self):
        self.experiment_list=[]
        self.graph_list=[]
        self.database={}
        self.total_graph_numbers=0
        
    def load_experiments(self,folder_path="database"):
        folder_path+="/*.graphml"
        #load graphml files in the folder
        path_list=glob.glob(folder_path)

        if len(path_list)==0:
            raise ValueError("no files found in ", folder_path)

        for i,path in enumerate(path_list):
            exp_data=ExperimentData(path)

            self.experiment_list.append(exp_data)
            self.graph_list.append(exp_data.g)

            #g,database_dict=exp_data.g,exp_data.experiment

            
            #allocate graph IDs for each record
            for k in exp_data.experiment.keys():
                exp_data.experiment[k]["graphID"]=self.total_graph_numbers
            
            #integrate experiment data
            if self.total_graph_numbers==0:
                self.database=exp_data.experiment
            else:
                for k,v in exp_data.experiment.items():
                    self.database[k]=v
            self.total_graph_numbers+=1
        
        
    def classify_experiments(self):
        graph_type_dict=categorize_graphs(self.graph_list)
        
        for k in self.database.keys():
            self.database[k]["graphID"]=graph_type_dict[self.database[k]["graphID"]]        
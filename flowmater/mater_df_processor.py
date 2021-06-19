from polysmiles.PolySMILES import PolySMILES
import pandas as pd


#unnecessary column for X
unnecessary_columns=[
    "graphID",
    "Env",
]

#chemical columns processed by polysmiles
chem_column_list=[
]

#categorical columns to be converted to numbers
to_numeric_dict={

}



class mater_df_processor:
    def __init__(self,
                y_column,
                unnecessary_columns=unnecessary_columns,
                chem_column_list=chem_column_list,
                to_numeric_dict=to_numeric_dict,
                psm=PolySMILES(),
                fill_mean=True
                ):
    
        self.y_column=y_column
        self.unnecessary_columns=unnecessary_columns
        self.chem_column_list=chem_column_list
        self.to_numeric_dict=to_numeric_dict
        self.psm=psm
        self.psm.dict_mode=False
        self.fill_mean=fill_mean
        
        self.nan_columns=[]
        self.initial_call=True
        
    def __call__(self,df):
        return self._process(df)
    
    def _process(self,df):
        
        #characters to numeric
        for col,dic in self.to_numeric_dict.items():
            for k,v in dic.items():
                df[col]=df[col].replace(k,v)


        #del records without y
        reg_df=df.dropna(axis=0,how="any",subset=self.y_column)

        #fill nan by mean
        if self. fill_mean:
            reg_df=reg_df.fillna(reg_df.mean())

        #calc chems
        reg_df=self._chem_to_num(reg_df)

        
        #X column
        X_column=list(reg_df.drop(self.y_column,axis=1).columns)

        #del unnecesary columns
        for c in self.unnecessary_columns:
            try:
                X_column.remove(c)
            except:
                print(c, "not in column")

                
        #del all nan columns
        if self.initial_call:
            self.nan_columns=list(reg_df.columns[reg_df.isnull().all()])        
            print("following columns won't be used because all data are nan", self.nan_columns)
            self.initial_call=False
            
        for c in self.nan_columns:
            X_column.remove(c)
        
        
        #set X,y
        X=reg_df[X_column]
        y=reg_df[self.y_column]
        
        #to numeric
        X=self._to_numeric(X)
        
        try:
            y=y.astype(float)
        except:
            print("y treated as categorical")
    
        return X,y
    
    def _to_numeric(self,num_X):
    
        #to numetic
        for c in num_X.columns:
            try:
                num_X[c]=num_X[c].astype(float)
            except:
                print("column ", c, " column treated as categorical variables")
        
        return num_X
    
    #convert smiles to numvers
    def _chem_to_num(self,X):
        
        num_X=X

        for chem_column in self.chem_column_list:
            print("process: ",chem_column)
            chem_df=self.psm.auto(X[chem_column])
            chem_df.columns=[i+"_"+chem_column for i in chem_df.columns]

            sm_column='SMILES'+"_"+chem_column
            chem_summary_df=chem_df.drop_duplicates(sm_column)

            #integrate to dataframe
            num_X=pd.merge(num_X, chem_summary_df,left_on=chem_column, right_on=sm_column)    

            #delete smiles columns
            num_X=num_X.drop(chem_column,axis=1)
            num_X=num_X.drop(sm_column,axis=1)    

        return num_X
    

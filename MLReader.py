from email import header
import logging
import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),"../../"))
import numpy as np
import pandas as pd
import sqlite3
import re
from Common.Library.FilePath import FilePath
from Common.Office.ExcelWrapper import ExcelWrapper
from Common.Library.CustomException import CustomException

class MLReader():
    '''
    input can be excel, csv, tabbed text, DataFrame,Series, sqllite 
    Note: In Sqlite: Data Source=<fullpath>;Table=<TableName>;...
    '''
    
    def __read_sqlite(self, databasepath):
        m = [x.split("=") for x in databasepath.split(";") if "=" in x]
        d = {x[0].strip():x[1].strip() for x in m}
        con = sqlite3.connect(d["Data Source"])
        df = pd.read_sql_query(f"SELECT * from {d['Table']}", con)
        con.close()
        return df
    
    def __read_excel(self):
        r,c = ExcelWrapper(self.__file.path).get_first_cell()
        if(r==-1 or c==-1):
            raise CustomException("Starting Row Cell not found")
        file=pd.read_excel(self.__file.path, header=r-1)
        for i in range(c-2,-1,-1):
            file.drop(columns=file.columns[i],inplace=True)
        return file
    
    def __read_csv(self):
        txt = self.__file.first_line()
        if(";" in txt):
            file=pd.read_csv(self.__file.path,delimiter=r";")
        else:
            file=pd.read_csv(self.__file.path)
            
        return file

    def __read_singletxt(self):
        #single column data
        x = np.loadtxt(self.__file.path,delimiter = '\n\n', dtype=str)
        reshaped = x.reshape(-1,1)
        df = pd.DataFrame(data = reshaped)
        return df
    
    def __read_txt(self):
        txt = self.__file.first_line()
        if("\t" not in txt): #space delimited
            try:
                file=pd.read_csv(self.__file.path,delimiter=r"\s+",encoding = "ISO-8859-1")
            except pd.errors.ParserError:
                file=self.__read_singletxt()
        else: #tabbed data
            file=pd.read_csv(self.__file.path)
        return file
    def __init__(self, filepath, ifseries=False):
        '''
        Constructor
        '''
        if type(filepath) ==list:
            self.data = pd.DataFrame(filepath)
        elif type(filepath) == pd.DataFrame:
            self.data = filepath
        elif type(filepath) == pd.Series:
            self.data = pd.DataFrame(filepath)
        elif filepath.startswith("Data Source="):
            self.data = self.__read_sqlite(filepath)
        else:
            self.__file = FilePath(filepath)
            
            if(self.__file.is_excel()):
                file = self.__read_excel()
            elif(self.__file.is_csv()):
                if(self.__file.ext()==".csv"):
                    file = self.__read_csv()
                else:
                    file = self.__read_txt()
            else:
                try:
                    file = self.__read_txt()
                except Exception as ex:
                    logging.error(ex)
                    raise CustomException("File not supported")
            
            self.data = file.reset_index(drop=True)
        
        if ifseries:
            if len(self.data.columns) == 1:
                self.data  = self.data.iloc[:,0]
        
    def clean(self):
        self.fillna()
        self.removeunnamed()
    
    def fillna(self,rep=''):
        self.data.fillna(rep, inplace=True)
        
    def removeunnamed(self):
        self.data = self.data.loc[:, ~self.data.columns.str.contains('^Unnamed')]

    def groupby(self, idd, aggfuncs):
        self.groupdata = self.data.groupby(self.data[idd]).aggregate(aggfuncs)

    def add_formula_column(self, name, formula, type="",fill=None):
        sn = formula
        for m in re.finditer("@\[([^\]]+)[\]]",formula):
            sn=sn.replace(m.group(0),f'pd.to_datetime(x["{m.group(1)}"])')
        s = self.data.apply(lambda x: eval(sn), axis=1)
        s = self._applytype(s,type)
        if fill is not None:
            s=s.fillna(fill)
        self.data[name]=s

    def _applytype(self, s, type):
        if type == "duration":
            s = s.dt.days
        return s
        

if __name__ == "__main__":
    #file="sample\\Employee1.xlsx"
    file="sample\\TicketsPMA1.xlsx"
    file = os.path.join(os.path.dirname(__file__),file)
    mlr = MLReader(file)
    data = mlr.data
    print(data.head())
    print(data.columns)

    mlr.add_formula_column("newcolumn", "0 if @[Status] == 'Closed' else 1")

    print(data[["Status", "newcolumn"]].head())

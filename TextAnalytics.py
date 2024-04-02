import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__),"../"))

from Common.Library.ConfigurationSettings import GetTempFile 

from Common.MachineLearning.MLReader import MLReader
from Common.MachineLearning.MLUSClassification import MLUSClassification 
from Common.Interface.abstract_bot import Bot, OutputParam, InputParam
from Common.Library.CustomException import CustomException
from Common.NLP.RakeSimilarity import rake_encode,rake_similarity
import logging
class TextAnalytics(Bot):

    def execute(self, context:dict):
        logging.info(type(context))
        logging.info(context)
        returncontext = super().execute(context)
        try:
            f = context["filename"]
            mldata = MLReader(f).data[[context["column"]]]
            mldata.columns = ["X"]
            mldata["Cluster"] =  MLUSClassification(mldata["X"]).kmeans()
            fo = GetTempFile("cluster.csv")
            mldata.to_csv(fo)
            returncontext["outfile"] = fo
            return returncontext

        except Exception as ex:
            logging.exception('Exception %s' %(ex,))
            return super().errorcontext(returncontext, ex)
        


    def inputs(self) -> InputParam:
        e = super().inputs()
        d = {"filename": ["string", "None", "Path of the data file"]}
        return d | e

    
    def outputs(self) -> OutputParam:
        d = {"outfile": ["string", "None", "path of output csv"],
            "column":["string", "None", "column header for which clustering needs to be done"]}
        return d | super().outputs()

if __name__ == "__main__":
    import os
    file="sample\\TicketsPMA1.xlsx"
    file = os.path.join(os.path.dirname(__file__),file)
    col = "Notes"
    context = {"filename":file, "column":col}
    t = TextAnalytics()
    t.bot_init()
    o = t.execute(context)
    obj = MLReader(o["outfile"]).data
    print(obj.head())
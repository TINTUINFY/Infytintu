import os
from Common.Interface.abstract_bot import Bot
from Common.MachineLearning.MLReader import MLReader
from Common.MachineLearning.MLSklearnModel import MLSklearnModel


class StepsCreater(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            inputfile = executeContext['InputFile']
            
            path=os.path.abspath(inputfile)
            
            self.reader = MLReader(path)
            
            self.model = MLSklearnModel(self.reader.data)
            
            self.model.LinearModel()
            
            print(self.model.Predict())
            
            self.model.ShowHist()
            
            
                
            return {"Steps":"","Status":"Success"}
        except:
            import traceback
            formatted_lines = traceback.format_exc().splitlines()
            print(formatted_lines)
            return {'Steps':"",'Status':"Failed","Error":formatted_lines}

if __name__ == "__main__":
    context={"InputFile": "sample\\sample.csv",}
    
    bot_obj = StepsCreater() 
        
    bot_obj.bot_init()
    
    output = bot_obj.execute(context)
    
    print("Status is ",output['Status'])
    #print the returning output from after execution
    print("Steps Created are ",output['Steps'])
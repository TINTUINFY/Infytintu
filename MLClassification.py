import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),"../../"))
import tempfile
from Common.MachineLearning.MLReader import MLReader
from Common.MachineLearning.MLSklearnModel import MLSklearnModel
from Common.Visualisation.PandaCharts import PandaCharts


class MLClassification():

    def generate_model(self, data,target,predictiors=[],ignore=[],index=[], displaychart=False,imgfile=""):
        try:
            
            if len(predictiors)==0:
                predictiors = list(set(data.columns) - set(target + ignore+index))
                
            if index:
                for item in index:
                    data[item]=data[item].astype(str)
                i=",".join(index)
                data[i] = data[index].agg('-'.join, axis=1)
                data.drop(index,axis=1,inplace=True)
                data.set_index(i)
            
            data.drop(ignore,axis=1,inplace=True)
            
            data.dropna(inplace=True)
            
            if displaychart:
                pchart = PandaCharts(data[predictiors])
                pchart.visualize_data(imgfile)
            
            self.model = MLSklearnModel(data,target[0],predictiors,ratio=0.33)
            
            if self.model.preferred_method() == "linear":
                self.model.linear_model()
            else:
                self.model.logistic_model()
                
            print(self.model.error())
            
            
            if self.model.preferred_method() == "linear":
                print(self.model.equation())
            
            
            
            p = os.path.join(tempfile.gettempdir(),"Infosys","bots")
            if not os.path.isdir(p):
                os.makedirs(p)
            filename=os.path.join(p, "model.sav")
            self.model.save_model(filename)

                
            return 1
        except Exception as e:
            print(e)  
            raise

    def generate_output(self,x_data):
        p = os.path.join(tempfile.gettempdir(),"Infosys","bots")
        filename=os.path.join(p, "model.sav")
        self.model = MLSklearnModel( filename=filename)
        return self.model.predict_all(x_data)
        
if __name__ == "__main__":
    imgfile = os.path.join(tempfile.gettempdir(),"Visual1.png")
    file="sample\\modeldataset.csv"
    file = os.path.join(os.path.dirname(__file__),file)
    reader = MLReader(file)
    data = reader.data
    
    test = set(["Score"]) # ["Rank","Relevance","Score"]
            
    ignorelst = list(set(["Rank","Relevance","Score"])-test) + ['index', 'Unnamed: 0', "Main Primary Skills", \
        "Primary Skills", "Secondary Skills", "Primary Skills JD", "Desired Skills (Extracted)"]
    
    data["EX Infosyscian"] = data["EX Infosyscian"].astype("float64")
    data["Designation Compare"] = data["Designation Compare"].astype("float64")
    
    MLClassification().generate_model(data,list(test),ignore=ignorelst,index=["Requisition ID", "Candidate ID"],displaychart=True, imgfile=imgfile)

    print(imgfile)

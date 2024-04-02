import sys, os
from tracemalloc import stop ; sys.path.append(os.path.join(os.path.dirname(__file__),"../"))
from Common.Library.ConfigurationSettings import GetTempFile, ReadFromConfigFile, WriteToConfigFile
from Common.MachineLearning.MLReader import MLReader ; sys.path.append(os.path.join(os.path.dirname(__file__),"../"))
from Common.Interface.abstract_bot import Bot, OutputParam, InputParam
from Common.Library.CustomException import CustomException

import logging
import nltk
from nltk.sentiment import vader
from nltk.corpus import sentiwordnet as swn, stopwords
from string import punctuation

SECTION = "SentimentAnalysis"
ATTRIBUTEALGO = "Algo"

class SentimentAnalysis(Bot):
    def __init__(self) -> None:
        super().__init__()
        self.algo = ""
    
    def bot_init(self):
        print("initialisation starts here...")
        self.algo=ReadFromConfigFile(SECTION,ATTRIBUTEALGO,"naive")
        
    def execute(self, context:dict):
        logging.info(type(context))
        logging.info(context)
        returncontext = super().execute(context)
        try:
            if "traindata" in context:
                self.__traindata(context["traindata"],context.get("algorithm","naive"))
            else:
                result = self.__getsentiment(context["newdata"])
                returncontext["SentimentResult"]=result
            return super().passcontext(returncontext)
        except Exception as ex:
            logging.exception('Exception %s' %(ex,))
            return super().errorcontext(returncontext, ex)
    def __getsentiment(self, newdata):
        if self.algo == "":
            raise Exception("Model not trained or bot_init not initialised")
        
        if type(newdata) == str:
            data = MLReader(newdata).data
        else:
            fname = GetTempFile("tempdata.csv")
            f = open(fname, "w")
            tdata = [x + "\n" for x in newdata]
            f.writelines(tdata)
            f.close()
            data = MLReader(fname).data

        if self.algo == "vader":
            sia = vader.SentimentIntensityAnalyzer()
            result = [sia.polarity_scores(x)['compound'] for x in data[data.columns[0]]]
            return result
        elif self.algo == "senti":
            result = []
            stopword = set(stopwords.words("english") + list(punctuation))
            for row in data[data.columns[0]]:
                reviewPolarity = 0.0
                for word in row.lower().split():
                    if word in stopword:
                        continue
                    weight = 0.0
                    try:
                        common_meaning = list(swn.senti_synsets(word))[0]
                        if common_meaning.pos_score()>common_meaning.neg_score():
                            weight += common_meaning.pos_score()
                        else:
                            weight += common_meaning.neg_score()
                    except:
                        pass
                    reviewPolarity += weight
                result.append(reviewPolarity)
            return result
        else:
            raise CustomException("Algo not Supported")


    def __traindata(self, traindata, algorithm):
        if type(traindata) == str:
            data = MLReader(traindata).data
        else:
            fname = GetTempFile("tempdata.csv")
            f = open(fname, "w")
            f.writelines(traindata)
            f.close()
            data = MLReader(fname).data
        if algorithm.lower() == "vader":
            WriteToConfigFile(SECTION,ATTRIBUTEALGO,"vader")
            self.algo = "vader"
        elif algorithm.lower() == "senti":
            WriteToConfigFile(SECTION,ATTRIBUTEALGO,"senti")
            self.algo = "senti"
        else:
            raise CustomException("Algo not Supported")

    def bot_cleanup(self):
        print("clean up starts here...")
        
    def inputs(self) -> InputParam:
        d = super().inputs()
        e = {"traindata": ["list of string or string", "None", "data in csv format or path of csv file to train for the required model. This can be passed once and then same data can be used for result multiple times"],
            "algorithm":["string","Naive","Type of algorithm for SentimentAnalysis. Options are Vader, Senti, Naive"],
            "newdata": ["list of string", "None", "data in simple text format or path of txt file for which we want the sentiment"]}
        return d | e

    
    def outputs(self) -> OutputParam:
        d = super().outputs()
        return d | {"SentimentResult": ["list", "None", "status as positive\\negative"]}

        
if __name__ == "__main__":
    from Common.MachineLearning.MLReader import MLReader
    import pandas as pd
    import tempfile
    file="rt-polaritydata\\rt-polarity.neg"
    file = os.path.join(os.path.dirname(__file__),file)
    objneg=MLReader(file).data
    print(objneg.head())
    objneg.columns=["text"]
    objneg["rating"]="negative"
    file="rt-polaritydata\\rt-polarity.pos"
    file = os.path.join(os.path.dirname(__file__),file)
    objpos=MLReader(file).data
    objpos.columns=["text"]
    objpos["rating"]="positive"
    
    datamodel=pd.concat([objpos,objneg]).reset_index(drop=True)

    f = tempfile.gettempdir() + "\\" + "data.csv"
    datamodel.to_csv(f,index=False)
    
    context = {"traindata":f, "algorithm":"Vader"}
    t = SentimentAnalysis()
    t.bot_init()
    o = t.execute(context)
    t.bot_cleanup()
    print(o)

    datamodel.drop("rating",axis=1).to_csv(f,index=False)
    context = {"newdata":f}
    t = SentimentAnalysis()
    t.bot_init()
    o = t.execute(context)
    t.bot_cleanup()
    print(o)

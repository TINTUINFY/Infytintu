import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Common.Interface.abstract_bot import Bot, InputParam, OutputParam
from Common.Library.CustomException import CustomException
import pandas as pd
import re

class TestStepsGenerator(Bot):
    def bot_init(self):
        print("initialisation starts here...")

    def execute(self, context: dict):
        returncontext = super().execute(context)
        print("Inside Execute")

        user_path = context.get("path")

        try:

            #Coverting excel sheets into dataframe
            dfStories = pd.read_excel(user_path, sheet_name="User_Story")
            dfNoun = pd.read_excel(user_path, sheet_name="Nouns")
            dfVerb = pd.read_excel(user_path, sheet_name="Verbs")
            dfURLs = pd.read_excel(user_path, sheet_name="URLs")

            # Converting Dataframes into Dict
            Nouns = {}
            Verbs = {}
            Urls = {}

            for i in range(len(dfNoun)):
                Nouns[dfNoun['Nouns'][i]] = {"Username":dfNoun['Username'][i],"Password":dfNoun['Password'][i]}
                
            for i in range(len(dfVerb)):
                Verbs[dfVerb['Verbs'][i].lower()]=dfVerb['Test Steps'][i].split(",")
                
            for i in range(len(dfURLs)):
                Urls[dfURLs['Webpage'][i].lower()] = dfURLs['URL'][i]

            #Generating Test Steps for each User story
            Generated_Steps = {}
            
            for i in range(len(dfStories)):
                UserStory = dfStories['User Story'][i]
                raw=[]
                Steps =[]
                #Extracting Noun, Verbs, Urls from the User Story
                try:
                    Noun = re.findall('!.*!',UserStory)[0].strip("!")
                    URL = re.findall('<.*>',UserStory)[0].strip("<>").lower()
                    Verblist = [i.strip("{}") for i in re.findall('{[a-zA-Z]*}',UserStory)]
                except:
                    raise CustomException("Please provide a valid User Story")

                for i in Verblist:
                    if i in Verbs:
                        for value in Verbs[i]:
                            step = value.replace("<<URL>>",Urls[URL]).\
                                    replace("[Username]",Nouns[Noun]["Username"]).\
                                    replace("[Password]",Nouns[Noun]["Password"].translate("*"*256))
                            if step not in raw: 
                                raw.append(step)
                
                for i,value in enumerate(raw):
                    x = f"Step{i+1}: {value.strip()}"
                    Steps.append(x)

                Generated_Steps[UserStory] = Steps

            #Converting Dict into DataFrame and exporting it as excel file
            final = pd.DataFrame()
            final["User Story"] = Generated_Steps.keys()
            final["Test Steps"] = Generated_Steps.values()

            try:
                if context.get('Outputname'):
                    final.to_excel(context.get('filename'))
                else:
                    final.to_excel("Output.xlsx")
            except:
                raise CustomException("Invalid filename")

            returncontext["status"] = "success"  
            return returncontext

        except Exception as e:
            return self.errorcontext({}, e)


    def input(self) -> InputParam:
        d = super().input()
        e = {"path": ["string", "None", "Valid path for xlsx file"],
                "Outputname": ["string", "None", "This name is used for excel file which we will get as an output"],
                }
        return d | e

    def notes(self):
        return """This is a Test Step Generator Bot. This bot takes excel as an input from which it read User stories and as an output it
        gives an excel of all User Stories with generated Test Steps.The report files will be available in the temporary directory.
        """    

    def outputs(self) -> OutputParam:
        d = super().outputs()
        e = {"success": ["string", "None", "The excel file of Test Steps successfully generated or not."]}
        return d | e 

if __name__ == "__main__":
    filename = "raw.xlsx"
    path = os.path.join(os.path.dirname(__file__),filename)
    context = {"path": path,
                "Outputname":"GeneratedTestCases.xlsx"}
    r = TestStepsGenerator()
    r.bot_init()
    r.execute(context)
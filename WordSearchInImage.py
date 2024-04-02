import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from Common.Interface.abstract_bot import Bot, InputParam, OutputParam
from Common.Library.CustomException import CustomException
from Common.OCR.DoctrOCR import DoctrOCR

class WordSearchInImage(Bot):
    
    def bot_init(self):
        return super().bot_init()
    
    def execute(self, context: dict):
        imageFilePath = context['imageFilePath']
        wordToSearch = context['wordToSearch']
        linesWithCoordinates = {}
        sentences = []
        try:
            json_output = DoctrOCR.imageToText(self,imageFilePath=imageFilePath)
            height = json_output['pages'][0]['dimensions'][0]
            width = json_output['pages'][0]['dimensions'][1]
            for block in json_output['pages'][0]['blocks']:
                for line in block['lines']:
                    sentence = ""
                    for value in line['words']:
                        sentence+=f" {value['value']}"
                    if wordToSearch.lower() in sentence.lower():
                        x_start = int(block['geometry'][0][0]*width)
                        y_start = int(block['geometry'][0][1]*height)
                        x_end = int(block['geometry'][1][0]*width)
                        y_end = int(block['geometry'][1][1]*height)
                        sentences.append({
                            "line":sentence,
                            "coordinates":[x_start,y_start,x_end,y_end]})
            if not sentences:
                raise CustomException("no line found for the given word")
            linesWithCoordinates['linesWithCoordinates'] = sentences
            return self.passcontext(linesWithCoordinates)
        except Exception as e:
            return self.errorcontext({}, e)
    
    def input(self) -> InputParam:
        d = super().input()
        e = {"imagepath": ["string", "None", "Valid Path of the image file in valid image format. Cannot be empty"],
            "wordToSearch":['String',"None","word to search in image. Cannot be empty"]}
        return d | e        

    def output(self) -> OutputParam:
        d = super().output()
        e = {"linesWithCoordinates": ["list of dict", "None", "every dictionary have line having wordToSearch within with coordinates"]}
        return d | e 
            
    def notes(self):
        return """Input to the bot will be a Image file along with the word to search in the image.The bot will extract the lines from the image having word along with the coordinates"""
        

if __name__ == "__main__":
    imageFileName = "messageBox.jpg"
    imageFilePath = os.path.join(os.path.dirname(__file__),"sample",imageFileName)
    context={
        "imageFilePath":imageFilePath,
        "wordToSearch":"error"
        }
    Bobj = WordSearchInImage()
    print(Bobj.execute(context=context))
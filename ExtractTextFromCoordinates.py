import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from Common.Interface.abstract_bot import Bot, InputParam, OutputParam
from Common.Library.CustomException import CustomException
from Common.TextExtractionTranslation.GetLanguageCode import GetLanguageCode
from Common.OCR.PytesseractOCR import PytesseractOCR
import cv2

class ExtractTextFromCoordinates(Bot):
    
    def bot_init(self):
        return super().bot_init()
    
    def execute(self, context: dict):
        imageFilePath = context['imagepath']
        language = context['language']
        tesserectPath = context['tesseractpath']
        coordinates = context['coordinates']
        textInCoordinates = {}
        try:
            if len(coordinates) < 4 or len(coordinates) < 4:
                raise CustomException("Please provide all 4 coordinates properly")
            else:
                x_start,y_start,x_end,y_end = coordinates
                langCode = GetLanguageCode.language_code(self,language=language)
                if not os.path.exists(imageFilePath):
                    raise CustomException("Provided file path not found")
                img = cv2.imread(imageFilePath)
                crop_img = img[int(y_start):int(y_end), int(x_start):int(x_end)]
                text = PytesseractOCR.imageToText(self,image=crop_img,langCode=langCode,tesseractPath=tesserectPath,imageFilePath=None)
                textInCoordinates['textInCoordinates'] = text
                return self.passcontext(textInCoordinates)
        except Exception as e:
            return self.errorcontext({},e)
    
    def input(self) -> InputParam:
        d = super().input()
        e = {"imagepath": ["string", "None", "Valid Path of the image file in valid image format. Cannot be empty"],
            "language": ["string", "None", "Language of the text present in the image. Cannot be empty."],
            "tesseractpath": ["string", "None", "Valid Path to tesseract.exe package in your directory. Cannot be empty."],
            "coordinates":['list of integer',"None","Coordinates within you want to extract text (format:[x_start,y_start,x_end,y_end])"]}
        return d | e        

    def output(self) -> OutputParam:
        d = super().output()
        e = {"textInCoordinates": ["string", "None", "Text extracted within the specified coordinates from the image"]}
        return d | e 
            
    def notes(self):
        return """This is a Text Extractor bot. The input to the bot will be a Image file.The bot will extract the text from the image file within the specified coordinates."""
        
if __name__ == "__main__":
    tesseractExePath ='D:\\Tesseract-OCR\\tesseract.exe'
    imageFileName = "FolderInUse.jpg"
    imagePath = os.path.join(os.path.dirname(__file__),"sample",imageFileName)
    context={
        "imagepath":imagePath,
        "language":"English",
        "tesseractpath":tesseractExePath,
        "coordinates":[38, 318, 426]}
    Bobj = ExtractTextFromCoordinates()
    print(Bobj.execute(context=context))
    
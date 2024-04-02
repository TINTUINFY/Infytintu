import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from Common.Interface.abstract_bot import Bot, InputParam, OutputParam
from Common.Library.CustomException import CustomException
from Common.TextExtractionTranslation.GetLanguageCode import GetLanguageCode
from Common.TextExtractionTranslation.ImageToText import ImageToText
from Common.TextExtractionTranslation.LanguageTranslator import LanguageTranslator
import os, pytesseract

class ImageTextTranslator(Bot):
    def execute(self, context: dict):
        returncontext = super().execute(context)
        tesseractpath = context.get("tesseractpath")
        path = context.get("imagepath")
        lang = context.get("language")
        code = GetLanguageCode().language_code(lang)

        try:
            image_to_text = ImageToText().extract_text(path, code, tesseractpath)
            print(image_to_text)
            text = LanguageTranslator().translate(image_to_text)
            returncontext["transltedtext"] = text  
            returncontext["status"] = "success"           
            return returncontext

        except FileNotFoundError:
            raise CustomException("File not found")

        except pytesseract.pytesseract.TesseractError:
            raise CustomException(f"{lang} language trained model not found in tessdata directory")

    def input(self) -> InputParam:
        d = super().input()
        e = {"imagepath": ["string", "None", "Valid Path of the image file in jpg format. Cannot be empty"],
                "language": ["string", "None", "Language of the text present in the image you want to translate to english. Cannot be empty."],
                "tesseractpath": ["string", "None", "Valid Path to tesseract.exe package in your directory. Cannot be empty."]}
        return d | e        

    def output(self) -> OutputParam:
        d = super().output()
        e = {"transltedtext": ["string", "None", "Text extracted from the image and translated into english language."]}
        return d | e 
            
    def notes(self):
        return """This is a Image to Text Translator bot. The input to the bot will be a Image file.
        The bot will extract the text from the image file and further translate the non english language to english.
        For non english text extraction from image the pre trained models are needed to be added to tessdata directory.
        The transaltion of the text to english language will not be 100% accurate but still give similar transaltion."""

if __name__ == "__main__":
    image = "Spanish.jpg"
    path = os.path.join(os.path.dirname(__file__),image)
    context = {"imagepath": path,
                "language":"spanish",
                "tesseractpath": r"C:\Users\pranjal.bhagat\AppData\Local\Tesseract-OCR\tesseract.exe"}
    r = ImageTextTranslator()
    r.bot_init()
    output = r.execute(context)
    print(output)
    
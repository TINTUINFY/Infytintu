import sys,os;sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Library.CustomException import CustomException
from Interface.iOCR import iOCR
import easyocr

class EasyOCR(iOCR):
    def imageToText(self, imageFilePath, langCode):
        """image to text conversion method using easyocr

        Args:
            imageFilePath (String): Path of input image file
            langCode (list of string): Language Codes of the text present in the image
            
        Returns:
            list: Details related to image
        """
        try:
            reader = easyocr.Reader(langCode)
            result = reader.readtext(imageFilePath)
            return result
        except Exception as e:
            raise CustomException(e)

if __name__ == "__main__":
    imageFileName = "FolderInUse.jpg"
    imagefilePath = os.path.join(os.path.dirname(__file__),"sample",imageFileName)
    langCode = ["en"]
    Bobj = EasyOCR()
    output = Bobj.imageToText(imageFilePath=imagefilePath,langCode=langCode)
    print(output)
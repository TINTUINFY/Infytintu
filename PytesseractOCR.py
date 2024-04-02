import sys,os;sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Library.CustomException import CustomException
from Interface.iOCR import iOCR
import cv2
from pytesseract import TesseractNotFoundError
import pytesseract

class PytesseractOCR(iOCR):
    def imageToText(self,imageFilePath,image,langCode,tesseractPath):
        """image to text conversion method using pytesseract

        Args:
            imageFilePath (String): Path of input image file
            langCode (String): Language Code of the text present in the image
            tesseractPath (String): Valid Path to tesseract.exe package in your directory.

        Returns:
            String: Return text grabbed from input image
        """
        """
        Page Segmentation modes:
        0 - Orientation and script detection (OSD) only. 
        1 - Automatic page segmentation with OSD.
        2 - Automatic page segmentation, but no OSD, or OCR. 
        3 - Fully automatic page segmentation, but no OSD. (Default) 
        4 - Assume a single column of text of variable sizes. 
        5 - Assume a single uniform block of vertically aligned text. 
        6 - Assume a single uniform block of text. 
        7 - Treat the image as a single text line. 
        8 - Treat the image as a single word.
        9 - Treat the image as a single word in a circle. 
        10 - Treat the image as a single character.
        11 - Sparse text. Find as much text as possible in no particular order. 
        12 - Sparse text with OSD. 
        13 - Raw line. Treat the image as a single text line.
        
        OCR Engine Mode
        0 - Legacy engine only.
        1 - Nueral nets LSTM engine only.
        2 - Legacy + LSTM engines.
        3 - Default, based on what is available
        
        """
        myconfig = r"--psm 11 --oem 3"
        
        try:
            pytesseract.pytesseract.tesseract_cmd = tesseractPath
            if imageFilePath:
                img = cv2.imread(imageFilePath)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return pytesseract.image_to_string(img_gray,config=myconfig, lang=langCode)
        except TesseractNotFoundError:
            raise CustomException("Invalid Path to tesseract.exe")
        except Exception as e:
            raise CustomException(e)
        
if __name__ == "__main__":
    imageFileName = "messageBox.jpg"
    imageFilePath = os.path.join(os.path.dirname(__file__),"sample",imageFileName)
    langCode = "eng"
    tessrectPath = 'D:\\Tesseract-OCR\\tesseract.exe'
    Bobj = PytesseractOCR()
    output = Bobj.imageToText(imageFilePath=imageFilePath,langCode=langCode,tesseractPath=tessrectPath)
    print(output)
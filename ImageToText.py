import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),"../../"))
import pytesseract
from pytesseract import TesseractNotFoundError
from PIL import Image, UnidentifiedImageError
from Common.Library.CustomException import CustomException

class ImageToText:
    def extract_text(self, path, code, tesseractpath):

        try:
            pytesseract.pytesseract.tesseract_cmd = tesseractpath
        except TesseractNotFoundError:
            raise CustomException("Invalid Path to tesseract.exe")

        try:
            image = Image.open(path)
        except UnidentifiedImageError:
            raise CustomException("Invalid file format")
        return pytesseract.image_to_string(image, lang=code)
         


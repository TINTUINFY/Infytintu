import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),"../../"))
from translate import Translator
from langdetect import detect

class LanguageTranslator:
    def translate(self, image_to_text):
        translate_code = detect(image_to_text)
        trans = Translator(to_lang="en", from_lang=translate_code)
        return trans.translate(image_to_text)
    
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Common.Interface.abstract_bot import Bot

from transformers import MarianMTModel, MarianTokenizer
from typing import Sequence

class Translator:
    def __init__(self, source_lang: str, dest_lang: str) -> None:
        self.model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{dest_lang}'
        self.model = MarianMTModel.from_pretrained(self.model_name)
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        
    def translate(self, texts: Sequence[str]) -> Sequence[str]:
        tokens = self.tokenizer(list(texts), return_tensors="pt", padding=True)
        translate_tokens = self.model.generate(**tokens)
        return [self.tokenizer.decode(t, skip_special_tokens=True) for t in translate_tokens]
        

class LanguageTranslation(Bot):
    """The bot is store and retrieve workflow specific configurations"""
    __version__ = "1.0.0"
    def execute(self, context: dict):
        returncontext = super().execute(context)
        try:
            input_text = context.get("input_text")
            input_language = context.get("input_language")
            self.register_variables(context)
            #TODO: Add your code
            marian_ru_en = Translator(input_language, 'en')
            translated_text = marian_ru_en.translate([input_text])
            # Returns: ['That being too conscious is a disease, a real, complete disease.']`    
            returncontext.update({"translated_text": translated_text})
            return returncontext
        except Exception as e:
            return self.errorcontext({}, e)
        
    def inputs(self):
        inputs = {
            "workflowname": ["string", "None", "Unique name for the workflow without any space. Max 20 alpha characters in lowercase (a-z)"],
            }
        return inputs | super().inputs()

    def outputs(self):
        d = {
            
        }
        return d | super().outputs()

    def helpers(self):
        h= super().helpers()
        h["errors"] = ""
        h["keywords"] = "configuration, settings"
        h["configuration"] = ""
        h["notes"] = "This bot can be used as workflow setting parameters like login credentials, database, pretrained model path, etc. Note: This needs to be called at start of the workflow and only once"
        return h

if __name__ == "__main__":
    bot_obj = LanguageTranslation()
    bot_obj.bot_init()
    context = {
        "input_language": "ru",
        "input_text": "что слишком сознавать — это болезнь, настоящая, полная болезнь."
        }
    print(bot_obj.execute(context=context))

import sys, os ; sys.path.append(os.path.join(os.path.dirname(__file__),"../"))
from Common.Interface.abstract_bot import Bot, OutputParam, InputParam
from Common.Library.CustomException import CustomException
from Common.NLP.BERTSimilarity import bert_encode, bert_similarity, bert_faiss_index, bert_faiss_similarity
from Common.NLP.RakeSimilarity import rake_encode,rake_similarity
import logging
class TextSimilarity(Bot):

    def execute(self, context:dict):
        logging.info(type(context))
        logging.info(context)
        returncontext = super().execute(context)
        try:
            
            typeencode = context.get("type","bert")
            encode = context.get("encode")
            if encode is None:
                text = context.get("text")
                if text is None:
                    raise CustomException("Incorrect Inputs")
                if typeencode == "bert":
                    encode = bert_encode(text)
                if typeencode == "faissbert":
                    encode = bert_encode(text)
                    bert_faiss_index(encode,"testing")
                if typeencode == "rake":
                    encode = rake_encode(text)
            returncontext["encode"] = encode
            comparetext = context.get("comparetext")
            if comparetext is not None and comparetext != "":
                if typeencode == "bert":
                    comparetext = bert_similarity(encode,comparetext)
                    returncontext["comparescore"] = comparetext
                if typeencode == "faissbert":
                    returncontext["comparerank"] = bert_faiss_similarity("testing", comparetext)
                if typeencode == "rake":
                    returncontext["comparescore"] = rake_similarity(encode,comparetext)
            return returncontext

        except Exception as ex:
            logging.exception('Exception %s' %(ex,))
            return super().errorcontext(returncontext, ex)
        


    def inputs(self) -> InputParam:
        d = super().inputs()
        e = {"type": ["string", "bert", "type of encoding or comparison. Options are bert, faissbert"],
            "encode":["list","None","list of encodings. Either encoding or text needs to be provided"],
            "text":["list","None","list of text to be encoded. Either encoding or text needs to be provided"],
            "comparetext":["string","None","text to be compared to encoding. if text is empty then comparision is not done"]}
        return d | e

    
    def outputs(self) -> OutputParam:
        d = super().outputs()
        return d | {"encode": ["list", "None", "encoding of text"],
            "comparescore":["list","None","compare score. if text is empty in input then None is retured"],
            "comparerank":["list","None","ranks in case of top 5 results"]}

if __name__ == "__main__":
    context = {"text":["A Graduate in Bachelor of Engineering having about 2 year 11 Months of IT experience, in Software industry. I am looking forward to built a career in an IT Company where I can develop and strengthen my technical skills and contribute very effectively to my company thereby achieving both professional and personal growth",
    "Experienced software engineer possesses mentoring skill and analytical focus. Sound communication skills and able to multitask. Has worked across various industry groups like CMT, Digital, Retail & APP."],
    "comparetext": "Need a software engineer for supporting operations",
    "type":"rake"
    }
    t = TextSimilarity()
    t.bot_init()
    o = t.execute(context)
    print(o)

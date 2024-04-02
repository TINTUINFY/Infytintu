import torch
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from nltk.tokenize      import word_tokenize, sent_tokenize
from nltk.corpus        import stopwords
from scipy.spatial              import distance

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')
stop_words      = stopwords.words('english')  


Vector = list[float]
ListVectors = list[Vector]

def gpt2_encode(lsttxt:list[str]) -> ListVectors:
    lstupdatedtxt = [tokenizer.encode(clean_text(text), return_tensors='pt') for text in lsttxt] #"tf" for tensor
    return [model.generate(x, max_length=200, do_sample=True) for x in lstupdatedtxt]

def gpt2_encodetext(txt) -> Vector:
    return gpt2_encode([txt])[0]

def gpt2_similarity(lstencodes, txt) -> list[float]:
    entxt = gpt2_encodetext(txt)
    return [ np.sum(1 - distance.cdist(en, entxt,"cosine")) for en in lstencodes]


def clean_text(text) -> list[str]:
    
    # Convert to sentences 
    text        = sent_tokenize(text)
    
    # Convert to lowercase
    text        = [sentence.lower() for sentence in text]
    
    # split into words
    words       = [word_tokenize(sentence) for sentence in text]    

    # Remove all tokens that are not alphabetic and remove stopwords
    words       = [[word for word in sentence if word.isalpha() and not word in stop_words] for sentence in words]
    
    #lemmatizer  = WordNetLemmatizer()
    #words       = [[lemmatizer.lemmatize(word) for word in sentence] for sentence in words]
    
    text        = [' '.join(str(word) for word in sentence) for sentence in words]

    if (len(text) == 0):
        text.append('adding dummy text1 to avoid encoding errors')
        text.append('adding dummy text2 to avoid encoding errors')
    
    if (len(text) == 1):
        text.append('adding dummy text to avoid encoding errors')
    
    return text

if __name__ == "__main__":
    text = ["A Graduate in Bachelor of Engineering having about 2 year 11 Months of IT experience, in Software industry. I am looking forward to built a career in an IT Company where I can develop and strengthen my technical skills and contribute very effectively to my company thereby achieving both professional and personal growth",
    "Experienced software engineer possesses mentoring skill and analytical focus. Sound communication skills and able to multitask. Has worked across various industry groups like CMT, Digital, Retail & APP."]
    en = gpt2_encode(text)
    print(gpt2_similarity(en, "Need a software engineer for supporting operations"))

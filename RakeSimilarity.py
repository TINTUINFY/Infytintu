import numpy as np
from rake_nltk          import Rake
from nltk.tokenize      import word_tokenize
from nltk.corpus        import stopwords

Vectorstr = list[str]
ListVectorsStr = list[Vectorstr]

rake_nltk_var = Rake()

stop_words      = stopwords.words('english')    

def __extract_keyword(text):
    
    try:
        rake_nltk_var.extract_keywords_from_text(str(text))
    except ZeroDivisionError:
        text = ['Dummy Sentence 1','Dummy Sentence 2']
        rake_nltk_var.extract_keywords_from_text(str(text))

    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    return(' '.join(keyword_extracted))

def __get_cosine_score_rake(X,Y):

    l1, l2  = [],[]
    # remove stop words from the string
    X_set, Y_set = {w for w in word_tokenize(X) if not w in stop_words},{w for w in word_tokenize(Y) if not w in stop_words}

    # form a set containing keywords of both strings
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    return(cosine)

def rake_encode(lsttxt:list[str]) -> ListVectorsStr:
    return [__extract_keyword(text) for text in lsttxt]

def rake_encodetext(txt) -> Vectorstr:
    return rake_encode([txt])[0]

def rake_similarity(lstencodes, txt) -> list[float]:
    entxt = rake_encodetext(txt)
    return [ __get_cosine_score_rake(en,entxt) for en in lstencodes]



if __name__ == "__main__":
    text = ["A Graduate in Bachelor of Engineering having about 2 year 11 Months of IT experience, in Software industry. I am looking forward to built a career in an IT Company where I can develop and strengthen my technical skills and contribute very effectively to my company thereby achieving both professional and personal growth",
    "Experienced software engineer possesses mentoring skill and analytical focus. Sound communication skills and able to multitask. Has worked across various industry groups like CMT, Digital, Retail & APP."]
    en = rake_encode(text)
    print(en)
    print(rake_similarity(en, "Need a software engineer for supporting operations"))

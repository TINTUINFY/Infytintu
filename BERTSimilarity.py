import numpy as np
import faiss
from sentence_transformers      import SentenceTransformer
from nltk.tokenize      import word_tokenize, sent_tokenize
from nltk.corpus        import stopwords
from nltk.stem          import WordNetLemmatizer

from scipy.spatial              import distance
import os



sbert_model_name = 'all-MiniLM-L6-v2'
p = os.path.join(os.path.dirname(__file__),"models")
sbert_model = SentenceTransformer(sbert_model_name,cache_folder=p)
sbert_model.max_seq_length = 500
output_value = 'sentence_embedding'
stop_words      = stopwords.words('english')  

Vector = list[float]
ListVectors = list[Vector]

def bert_encode(lsttxt:list[str]) -> ListVectors:
    lstupdatedtxt = [clean_text(text) for text in lsttxt]
    return [sbert_model.encode(text,show_progress_bar=False,\
                            convert_to_numpy=True, batch_size = 64,\
                            normalize_embeddings = False,output_value=output_value) \
                            for text in lstupdatedtxt]

def bert_encodetext(txt) -> Vector:
    return bert_encode([txt])[0]

def bert_faiss_index(lstencodes, filename):
    npencodes = np.array([ np.mean(en, axis=0) for en in lstencodes])
    index = faiss.IndexIDMap(faiss.IndexFlatIP(384))
    index.add_with_ids(npencodes, np.array(range(0, len(npencodes))).astype(np.int64))
    faiss.write_index(index, filename)

def bert_similarity(lstencodes, txt) -> list[float]:
    entxt = bert_encodetext(txt)
    return [ np.sum(1 - distance.cdist(en, entxt,"cosine")) for en in lstencodes]

def bert_faiss_similarity(filename, txt, k=5):
    index = faiss.read_index(filename)
    entxt = bert_encodetext(txt)
    entxt = np.mean(entxt, axis=0)
    if len(entxt.shape) == 1:
      entxt = entxt.reshape(1,entxt.shape[0])
    top_k = index.search(entxt, k)
    return [_id for _id in top_k[1].tolist()[0]]

def clean_text(text) -> list[str]:
    
    # Convert to sentences 
    text        = sent_tokenize(text)
    
    # Convert to lowercase
    text        = [sentence.lower() for sentence in text]
    
    # split into words
    words       = [word_tokenize(sentence) for sentence in text]    

    # Remove all tokens that are not alphabetic and remove stopwords
    words       = [[word for word in sentence if word.isalpha() and not word in stop_words] for sentence in words]
    
    lemmatizer  = WordNetLemmatizer()
    words       = [[lemmatizer.lemmatize(word) for word in sentence] for sentence in words]
    
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
    en = bert_encode(text)
    bert_faiss_index(en,"testing")
    #print(en)
    print(bert_similarity(en, "Need a software engineer for supporting operations"))

    print(bert_faiss_similarity("testing", "Need a software engineer for supporting operations"))

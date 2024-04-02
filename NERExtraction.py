from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
import spacy
import pickle
import random
import os
from spacy.training.example import Example
from Common.Library.CustomException import CustomException
from Common.Library import FilePath


class NERExtraction():
    
    def __init__(self, name="nlp_model", file="", ifrecreate=False):
        
        if file != "" and (os.path.isdir(name) == False or ifrecreate==True):
            if(file.endswith("pkl")):
                data = pickle.load(open(file, "rb"))
            else:
                fp = open(file,"r", errors="ignore")
                txt = fp.read()
                lst = ",".join([x for x in txt.split("\n") if x !=""])
                data = list(eval(lst))
                fp.close()
            self.nlp = self.train_model(data)
            self.nlp.to_disk(name)
        else:
            if not os.path.isdir(name):
                raise CustomException("Incorrect Model")
            self.nlp = spacy.load(name)
            
    def clean_data(self,x):
        txt = x.lower()
        # remove trailing spaces
        txt = txt.strip()
        # tokenize 
        txt = word_tokenize(txt)
        # remove stop words
        stop = stopwords.words('english')
        txt = [w for w in txt if not w in stop] 
        return(" ".join(txt)) 
            
    def get_entities(self, txt):   
            doc = self.nlp(txt)
            for ent in doc.ents:
                print(f'{ent.label_.upper():{30}} - {ent.text}')
    
    def train_model(self, data):
        nlp = spacy.blank("en")
        if 'ner' not in nlp.pipe_names:
            ner = nlp.add_pipe("ner", last=True)
        
        for _,annotation in data:
            for ent in annotation['entities']:
                ner.add_label(ent[2])
                
        
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe !="ner"]
        with nlp.select_pipes(disable=other_pipes):
            optimizer = nlp.begin_training()
            for itn in range(10):
                print("start iteration " + str(itn))
                random.shuffle(data)
                losses = {}
                for text,annotations in data:
                    try:
                        doc = nlp.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        nlp.update(
                           [example],
                            drop=0.2,
                            sgd=optimizer,
                            losses=losses)
                    except Exception:
                        pass
                print(losses)
                
        return nlp
    
def test_ner():
    p = os.path.dirname(__file__)
    txt = FilePath.FilePath(os.path.join(p,"..\\..\\Inputs\\sampleresume.txt")).get_text()
    ne = NERExtraction("nlp_model",os.path.join(p,"..\\..\\Resources\\resume_train_data.txt"))
    ne.get_entities(txt)
if __name__ == '__main__':
    test_ner()
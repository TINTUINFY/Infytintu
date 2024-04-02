import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string

class Tokenization():

    def tokenizer(self, sentence):
        punctuation = string.punctuation
        ls = WordNetLemmatizer()
        #remove distracting single quotes
        sentence = re.sub('\'','',sentence)

        #remove digits adnd words containing digits
        sentence = re.sub('\w*\d\w*','',sentence)

        #replace extra spaces with single space
        sentence = re.sub(' +',' ',sentence)

        #remove unwanted lines starting from special charcters
        sentence = re.sub(r'\n: \'\'.*','',sentence)
        sentence = re.sub(r'\n!.*','',sentence)
        sentence = re.sub(r'^:\'\'.*','',sentence)
        
        #remove non-breaking new line characters
        sentence = re.sub(r'\n',' ',sentence)
        
        #remove punctunations
        sentence = re.sub(r'[^\w\s]',' ',sentence)
        
        #creating token object
        tokens = nltk.word_tokenize(sentence)
        
        #lower, strip and lemmatize
        tokens = [ls.lemmatize(word).lower().strip() for word in tokens]
        
        #remove stopwords, and exclude words less than 2 characters
        tokens = [word for word in tokens if word not in stopwords.words('english') and word not in punctuation and len(word) > 2]
        
        #return tokens
        return tokens
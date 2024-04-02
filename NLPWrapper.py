import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation

class NLPWrapper():
    
    __dictpos = {"CC":"Coordinating conjunction", "CD":"Cardinal number", 
                 "DT":"Determiner", 'EX':"Existential there", "FW":"Foreign word", 
                 "IN":"Preposition or subordinating conjunction", "JJ":"Adjective", 
                 "JJR":"Adjective, comparative", "JJS":"Adjective, superlative", 
                 "LS":"List item marker", "MD":"Modal", "NN":"Noun, singular or mass", 
                 "NNS":"Noun, plural", "NNP":"Proper noun, singular", 
                 "NNPS":"Proper noun, plural", "PDT":"Predeterminer", "POS":"Possessive ending", 
                 "PRP":"Personal pronoun", "PRP$":"Possessive pronoun", "RB":"Adverb", 
                 "RBR":"Adverb, comparative", "RBS":"Adverb, superlative", "RP":"Particle", 
                 "SYM":"Symbol", "TO":"to", "UH":"Interjection", "VB":"Verb, base form", 
                 "VBD":"Verb, past tense", "VBG":"Verb, gerund or present participle", 
                 "VBN":"Verb, past participle", "VBP":"Verb, non-3rd person singular present", 
                 "VBZ":"Verb, 3rd person singular present", "WDT":"Wh-determiner", 
                 "WP":"Wh-pronoun", "WP$":"Possessive wh-pronoun", "WRB":"Wh-adverb"}
    
    def __init__(self, text):
        self.text = text
        self.sents=sent_tokenize(text)
        self.words=word_tokenize(text)
        self.__customStopWords=set(stopwords.words('english')+list(punctuation))
        self.wordswostop=[word for word in word_tokenize(text) if word not in self.__customStopWords]
        postag=nltk.pos_tag(self.words)
        self.pos=[(tag[0], tag[1], NLPWrapper.__dictpos[tag[1]] ) if tag[1] in NLPWrapper.__dictpos.keys() else (tag[0], tag[1] ) for tag in postag]
        
    def GetBiDiagrams(self):
        from nltk.collocations import BigramCollocationFinder
        #biagram_measures = nltk.collocations.BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(self.wordswostop)
        return sorted(finder.ngram_fd.items())
        
if __name__ == "__main__":
    test = NLPWrapper("mary closed on closing night when she was in the mood to close.")
    print(test.pos)
    print(test.GetBiDiagrams())
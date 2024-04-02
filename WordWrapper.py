import docx2txt

class WordWrapper():
    
    def __init__(self, file):
        self.filename = file
        
    def read_word_resume(self):
        resume = docx2txt.process(self.filename)
        resume = str(resume)
        #print(resume)
        text =  ''.join(resume)
        text = text.replace("\n", "")
        if text:
            return text
    
    
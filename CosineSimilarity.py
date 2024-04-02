import re
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords

class CosineSimilarity():
    
    def __init__(self,text1, text2):
        self.text = [self.clean_txt(text1),self.clean_txt(text2)]
    
    def cosine_similarity(self):
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        cv = CountVectorizer(stop_words='english')
        count_matrix = cv.fit_transform(self.text)
        
        match_percentage = cosine_similarity(count_matrix)[0][1] * 100
        match_percentage = round(match_percentage, 2) # round to two decimal
        
        return match_percentage
    
    def clean_txt(self, txt):
        ''' a function to create a word cloud based on the input text parameter'''
        ## Clean the Text
        # Lower
        clean_jd = txt.lower()
        # remove punctuation
        clean_jd = re.sub(r'[^\w\s]', '', clean_jd)
        # remove trailing spaces
        clean_jd = clean_jd.strip()
        # remove numbers
        clean_jd = re.sub('[0-9]+', '', clean_jd)
        # tokenize 
        clean_jd = word_tokenize(clean_jd)
        # remove stop words
        stop = stopwords.words('english')
        clean_jd = [w for w in clean_jd if not w in stop] 
        return(" ".join(clean_jd))
    
if __name__ == '__main__':
    import os
    p1= os.path.abspath("..\\..\\Inputs\\candidate_resumes\\1001484967-.pdf.txt")
    with open(p1, 'r', errors="ignore") as f:
            t1 = f.read().lower()
    t2="""A day in the life of an Infoscion
As part of the Infosys project management team, your primary role would be to take end-to-end bottom line responsibility for a Project. 
You will lead the proposal preparation, review the project estimations, capture inputs from key stakeholders to position Infosys suitably in order to seal the deal. 
You will schedule assignments, monitor, review and report project status regularly in order to manage project risks and ensure successful project delivery and implementation. 
You will also coach and create a vision for the team, provide subject matter training for your focus areas, motivate and inspire team members through effective and timely feedback and recognition for high performance. 
You would be a key contributor in creating thought leadership within the area of technology specialization and in compliance with guidelines, policies and norms of Infosys.
If you think you fit right in to help our clients navigate their next in their digital transformation journey, this is the place for you!  Primary skills:Java
Desirables:Java->Core Java,Springboot Project Management fundamentals 
Project Lifecycles on development & maintenance projects, estimation methodologies, quality processes.
Knowledge of one or more programming languages; knowledge of architecture frameworks, and design principles; ability to comprehend & manage technology, performance engineering.
Domain 
Basic domain knowledge in order to understand the business requirements / functionality.
Ability to perform project planning and scheduling, manage tasks and coordinate project resources to meet objectives and timelines 
Ability to work with business and technology subject matter experts to assess requirements, define scope, create estimates, and produce project charters 
Good understanding of SDLC and agile methodologies is a pre-requisite
Awareness of latest technologies and trends
Logical thinking and problem solving skills along with an ability to collaborate
"""
    t = CosineSimilarity(t1,t2)
    print(t.cosine_similarity())
    
    t = CosineSimilarity("good boy is hi", "good girl")
    print(t.cosine_similarity())
    
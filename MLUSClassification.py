from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction.text import TfidfVectorizer

class MLUSClassification:
    def __init__(self, X, algo="tfid") -> None:

        
        
            
        self.X = X.fillna('')
        self.algo = algo

    def extractkeywords(self, lst):
        """extract the keywords from the list of strings
        example lst:
        not able to login in salesforce
        salesforce is not launching"""
        



    def kmeans(self, clusters=None):
        if self.algo == "tfid":
            vectorizer=TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
        elif self.algo == "rake":
            pass #mldata["Rake"] = mldata.apply(lambda x: rake_encode(x["x"]), axis=1)
        else:
            vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
        
        
        v= vectorizer.fit_transform(self.X)
        if clusters is None:
            silhouette_avg = []
            ly_km = []
            limit = max(11, len(self.X))
            for clusters in range(3, limit):
                km = KMeans(n_clusters=clusters,init= 'k-means++', max_iter=100, n_init=1)
                y_km = km.fit_predict(v)
                cluster_labels = km.labels_
                silhouette_avg.append(silhouette_score(v, cluster_labels))
                ly_km.append(y_km)
            m = max(silhouette_avg)
            i = silhouette_avg.index(m)
            y_km = ly_km[i]
            
        else:
            km = KMeans(n_clusters=clusters,init= 'k-means++', max_iter=100, n_init=1)
            y_km = km.fit_predict(v)

        return y_km
    
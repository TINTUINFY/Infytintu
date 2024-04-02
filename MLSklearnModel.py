from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
import pandas as pd
import pickle

class MLSklearnModel():
    
    def load_model(self,filename):
        (self.model,self.le,self.predictors,self.type) = pickle.load(open(filename, 'rb'))
        
    def save_model(self, filename):
        # save the model to disk
        pickle.dump((self.model,self.le,self.predictors,self.type), open(filename, 'wb'))

    def __init__(self, dataframe=None, target="",predictors=None,ratio=0.2, filename=""):
        if predictors is None:
            predictors = []
        if filename:
            self.load_model(filename)
            return 
        if len(predictors)==0:
            Y = dataframe[target]
            X= dataframe.drop(columns=[target])
        else:
            Y = dataframe[target]
            X= dataframe[predictors]
            
        if len(Y.unique())<=5:
            self.le = LabelEncoder()
            Y = Y.to_frame().apply(self.le.fit_transform).iloc[:,0]
        else:
            self.le = None
            
        self.predictors = predictors
        
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(X,Y, test_size=ratio, random_state=0)
        
        self.type = 0
        
        
    def preferred_method(self):
        if len(self.y_train.unique()) > 5:
            return "linear"
        else:
            return "logistic"
        
    def Standar_scalar(self):
        scaler = StandardScaler()
        self.x_train[:] = scaler.fit_transform(self.x_train)
        self.x_test[:] = scaler.transform(self.x_test)
        return scaler

    def ShowHist(self):
        self.y_train.hist(bins=50, figsize=(20,15))
        plt.show()
        
    def linear_model(self):
        from sklearn.linear_model import LinearRegression
        self.model = LinearRegression()
        self.model.fit(self.x_train,self.y_train)
        self.type=2

    def neural_model(self):
        from sklearn.neural_network import MLPClassifier    
        self.model = MLPClassifier(early_stopping=True,random_state=0,verbose=2)
        self.model.fit(self.x_train,self.y_train)
        self.type=1
    

    def logistic_model(self):
        from sklearn.linear_model import LogisticRegression
        self.model = LogisticRegression()
        self.model.fit(self.x_train,self.y_train)
        self.type=1
    
    def random_forest_model(self, max_depth=None, min_samples_leaf=None, n_estimators=None,n_jobs=None):
        from sklearn.ensemble import RandomForestClassifier
        self.model = RandomForestClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf, n_estimators=n_estimators,n_jobs=n_jobs, random_state=42)
        self.model.fit(self.x_train,self.y_train)
        self.type=1
    
    def decision_tree_model(self):
        from sklearn.tree import DecisionTreeClassifier
        self.model = DecisionTreeClassifier(random_state=42)
        self.model.fit(self.x_train,self.y_train)
        self.type=1
    
    def gradient_boosting_model(self):
        from sklearn.ensemble import GradientBoostingClassifier
        self.model = GradientBoostingClassifier()
        self.model.fit(self.x_train,self.y_train)
        self.type=1
    
    def ada_boosting_model(self):
        from sklearn.ensemble import AdaBoostClassifier
        self.model = AdaBoostClassifier(algorithm="SAMME")
        self.model.fit(self.x_train,self.y_train)
        self.type=1
    
    def naive_bernoulli_nbmodel(self):
        from sklearn.naive_bayes import BernoulliNB
        self.model = BernoulliNB()
        self.model.fit(self.x_train,self.y_train)
        self.type=1
    
    def naive_gaussian_model(self):
        from sklearn.naive_bayes import GaussianNB
        self.model = GaussianNB()
        self.model.fit(self.x_train,self.y_train)
        self.type=1
    
    def ann_model(self):
        from sklearn.neural_network import MLPClassifier
        self.model = MLPClassifier()
        self.model.fit(self.x_train,self.y_train)
        self.type=1
    
    
    def svm(self):
        from sklearn.svm import SVC
        self.model = SVC(C=2,gamma="auto",probability=True,kernel="sigmoid",shrinking=True,random_state=42)
        self.model.fit(self.x_train,self.y_train)
        self.type=1
        
    def svr_poly(self):
        from sklearn.svm import SVR
        self.model = SVR(kernel="linear", gamma="scale",epsilon=5)
        self.model.fit(self.x_train,self.y_train)
        self.type=2
    
    def error(self):
        if len(self.x_train)==0:
            return 
        from sklearn.metrics import mean_squared_error,f1_score
        
        if len(self.x_train)>0:
            train_predictions = self.model.predict(self.x_train)
            train_err=np.sqrt(mean_squared_error(self.y_train, train_predictions))
        else:
            train_err="NA"
        
        test_predictions = self.model.predict(self.x_test)
        test_err=np.sqrt(mean_squared_error(self.y_test, test_predictions))
                
        if len(self.x_train)>0:
            coeffofdettrain = self.model.score(self.x_train,self.y_train)
        else:
            coeffofdettrain="NA"
            
        if self.type == 1:
            f1score_train=f1_score(self.y_train, train_predictions, average='weighted')
            f1score_test=f1_score(self.y_test, test_predictions, average='weighted')
        else:
            f1score_train = "NA"
            f1score_test = "NA"
            
        coeffofdettest = self.model.score(self.x_test,self.y_test)

        
        n = "Adjusted R-Square" if self.type==2 else "Accuracy"
        
        return {"mean square":{"train":train_err,"test":test_err},
                n:{"train":coeffofdettrain,"test":coeffofdettest},
                "F1_Score":{"train":f1score_train,"test":f1score_test}}
    
    def equation(self):
        coef = self.model.coef_[0] if type(self.model.coef_[0]) is np.ndarray else self.model.coef_
        equatcoeff = ["{0}({1})".format(coef[i], self.x_train.columns[i]) for i in range(len(self.x_train.columns))]
        return {"Intercept":self.model.intercept_,"Coefficient":self.model.coef_,
                "equation":"{0} + {1} + e".format(self.model.intercept_, 
                " + ".join(equatcoeff))}
    
    def correlation(self):
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        vif = pd.Series([variance_inflation_factor(self.x_train.values, i) for i in range(len(self.x_train.columns)) ],
                        index=self.x_train.columns)
    
        return {"VIF":vif,"correlation Matrix":self.x_train.corr()}
    
    def predict_all(self,x):
        result = self.predict(x[self.predictors])
        if self.type == 1:
            prob, cls = self.predict_probality(x[self.predictors])
        else:
            prob = result
            cls = [0]
        return prob,cls, result
    
    def predict(self,x):
        y_pred =  self.model.predict(x)
        if self.le != None:
            y_pred = self.le.inverse_transform(y_pred)
        return y_pred
    
    def ScatterPlot(self):
        if self.X_train.shape[1] > 3:
            cols = 3
            rows = self.X_train.shape[1]//3+1
            fig,ax = plt.subplots(rows,cols)
            
        else:
            cols = self.X_train.shape[1]
            rows = 1
            fig,ax1 = plt.subplots(rows,cols)
            ax = [ax1] if cols > 1 else [[ax1]]
            
        for i in range(rows):
            for j in range(cols):
                if i*3+j < len(self.X_train.columns):
                    ax[i][j].scatter(self.X_train[self.X_train.columns[i*3+j]], self.Y_train)
            
        
        plt.show()
    
    def predict_probality(self,x):
        cls = self.model.classes_
        if self.le != None:
            cls = self.le.inverse_transform(cls)
        return self.model.predict_proba(x),cls
    
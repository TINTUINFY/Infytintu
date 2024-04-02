import nltk
from sklearn.impute import SimpleImputer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
class DataCleaningBot():
    def data_cleaning(self, my_file, cat_col=None, num_cols=None):
        impute_num = SimpleImputer(strategy="median") # Replace the Null vaues by median value
        impute_cat = SimpleImputer(strategy="constant", fill_value="NA") # Replace the Null vaues by constant value "NA"
        if cat_col:
            my_file[cat_col] = impute_cat.fit_transform(my_file[[cat_col]])
        if num_cols:
            my_file[num_cols] = impute_num.fit_transform(my_file[[num_cols]])
        return my_file # return the cleaned dataset

    def clean_text(self, row):
        stop_words=set(nltk.corpus.stopwords.words('english'))
        le=WordNetLemmatizer()
        row = row.replace("_", " ")
        word_tokens=word_tokenize(row)
        tokens=[le.lemmatize(w) for w in word_tokens if w not in stop_words and len(w)>2 and w.isalpha()]
        cleaned_text=" ".join(tokens)
        return cleaned_text


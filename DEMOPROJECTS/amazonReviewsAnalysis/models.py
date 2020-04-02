from django.db import models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import csv
import re
import string
string.punctuation

# Create your models here.
class Reviews:
    name:str
    comment:str
    email:str
    response:str
    reviews_count=[]
    def modelFit(self):
        data = pd.read_csv("Reviews.csv")
        data = data.loc[:, ['Summary','Text', 'Score', 'ProductId','HelpfulnessNumerator','UserId', 'HelpfulnessDenominator']]
        data["Sentiment"] = data["Score"].apply(lambda score: "positive" if score > 3 else "negative")
        data['Helpfulness'] = data['HelpfulnessNumerator']/data['HelpfulnessDenominator']
        #data.dropna(subset=['Summary'], inplace=True)
        data['Text_Clean']=data['Text'].apply(self.cleanup)
        df=data[data['Score']!=3]
        tfidf_transformer = TfidfVectorizer(ngram_range=(1,2), stop_words='english')
        reviews_tfidf = tfidf_transformer.fit_transform(df['Text_Clean'])
        X = reviews_tfidf
        y = df['Sentiment']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        logmodel = LogisticRegression()
        model_fit = logmodel.fit(X_train, y_train)
        returnValue = [model_fit,tfidf_transformer,data]
        return returnValue

    def cleanup(self,sentence):
        cleanup_re = re.compile('[^a-z]+')
        sentence = sentence.lower()
        sentence = cleanup_re.sub(' ', sentence).strip()
        return sentence



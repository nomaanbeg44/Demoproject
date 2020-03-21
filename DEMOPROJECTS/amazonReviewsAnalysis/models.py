from django.db import models
from sklearn.feature_extraction.text import CountVectorizer
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
    def modelFit(self):
        data = pd.read_csv("Reviews.csv")
        df = data.loc[:, ['Summary', 'Score', 'HelpfulnessNumerator', 'HelpfulnessDenominator']]
        df.dropna(subset=['Summary'], inplace=True)
        df = df[df['Score'] != 3]
        df["Sentiment"] = df["Score"].apply(lambda score: "positive" if score > 3 else "negative")
        df["Summary_Clean"] = df["Summary"].apply(self.cleanup)
        vectorizer = CountVectorizer(ngram_range=(1, 2))
        reviews_tfidf = vectorizer.fit_transform(df['Summary_Clean'])
        X = reviews_tfidf
        y = df['Sentiment']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        logmodel = LogisticRegression()
        model_fit = logmodel.fit(X_train, y_train)
        returnValue = [model_fit,vectorizer,df]
        return returnValue

    def cleanup(self,sentence):
        cleanup_re = re.compile('[^a-z]+')
        sentence = sentence.lower()
        sentence = cleanup_re.sub(' ', sentence).strip()
        # sentence = " ".join(nltk.word_tokenize(sentence))
        return sentence



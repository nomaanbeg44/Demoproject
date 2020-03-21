from django.shortcuts import render
from django.http import HttpResponse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from sklearn.linear_model import LogisticRegression
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import re
import string
string.punctuation
from .models import Reviews
revs= Reviews()
k=[]
# Create your views here.

def home(request):
    k.extend(revs.modelFit())
    return render(request, 'homepage.html')

def login(request):
    return render(request, 'login.html')

def homepage(request):
    return render(request, 'homepage.html')

def visualization(request):
    email=request.POST["email"]
    password=request.POST["pass"]
    if email=='a@a.com' and password=='admin':
        return render(request, 'adminPage.html')
    else:
        return render(request, 'login.html')
    #return render(request, 'visualizationPage.html') if email=='admin@amazon.com' and password=='amazon@123' else return render(request, 'homepage.html')

def getfigure(request):
    data=k[2]
    group = data.groupby('Sentiment')['Summary'].count()
    col=['Negative', 'Positive']
    count=[group.negative, group.positive]
    output_file("reviewCount.html")
    p = figure(x_range=col, plot_height=250, title="Total positive and Negative Reviews",
               toolbar_location=None, tools="")
    p.vbar(x=col, top=count, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    script, div =components(p)
    #print(script)
    #return render(request, 'visualizationPage.html', {'script':script, 'div':div})
    show(p)
    return render(request, 'adminPage.html')


def about(request):
    return render(request, 'about.html')

def comments(request):

    revs.name = request.POST["customer_name"]
    revs.comment = request.POST["customer_comment"]
    #resp=revs.resposeToCustomer(k, name, comment)
    vectorizer=k[1]
    logmodel=k[0]
    sample_vectorizer = vectorizer.transform([revs.comment])
    Sample_prediction = logmodel.predict(sample_vectorizer)
    if Sample_prediction=='positive':
        revs.response="Hello "+revs.name+ ", We are glad that you liked our service"
    else:
        revs.response = "Hello "+revs.name+ ", we are sorry that you are not satisfied with our service."
    return render(request, 'resultspage.html', {'result':revs})


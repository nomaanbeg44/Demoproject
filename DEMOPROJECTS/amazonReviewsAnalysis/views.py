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
    data=k[2]
    genuine_reviews= round((len(data[ data['Helpfulness']>.50 ])/len(data)),2)
    revs.reviews_count=[round((len(data[ (data['Score']==4) | (data['Score']==5) ])/len(data)),2),
                       round((len(data[ (data['Score']==1) | (data['Score']==2) ])/len(data)),2),
                       round((len(data[data['Score']==3])/len(data)),2),
                       genuine_reviews ]
    email=request.POST["email"]
    password=request.POST["pass"]
    if email=='a@a.com' and password=='admin':
        return render(request, 'adminPage.html',{'loader': revs})
    else:
        return render(request, 'login.html')

def getPlot1(request):
    # plot for total positve and negative
    data=k[2]
    group = data.groupby('Sentiment')['Text'].count()
    col=['Positive', 'Negative']
    count=[group.positive, group.negative]
    p = figure(x_range=col, plot_height=250, title="Total positive and Negative Reviews",
               toolbar_location=None, tools="")
    p.vbar(x=col, top=count, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    script, div =components(p)
    show(p)
    return render(request, 'adminPage.html',{'loader': revs})

def getPlot3(request):
    # plot for total reviews for each score
    data=k[2]
    score_df = data['Score'].value_counts(ascending = False).rename_axis('Score').reset_index(name='Counts').sort_values('Score',ascending=False)
    p = figure(x_range=score_df['Score'].astype(str).tolist(), plot_height=450, title="Score Counts",
           toolbar_location=None, y_range=(0,400000),lod_interval = 50000)
    p.vbar(x=score_df['Score'].astype(str).tolist(), top=score_df['Counts'].tolist(), width=0.9)
    p.left[0].formatter.use_scientific = False
    show(p)
    return render(request, 'adminPage.html',{'loader': revs})

def getPlot4(request):
    # plot for top 20 users
    data=k[2]
    top_users = data['UserId'].value_counts().head(20).rename_axis('UserId').reset_index(name='Total_Reviews')
    i3 = top_users.set_index('UserId').index
    i4 = data.set_index('UserId').index
    top_users = pd.merge(top_users,
                         data[i4.isin(i3)].groupby('UserId')['Helpfulness'].mean().rename_axis('UserId').reset_index(name='Avg_Helpfulness_percentage'),
                         on="UserId")
    top_users['Avg_Helpfulness_percentage'] = 100 * top_users['Avg_Helpfulness_percentage']
    p = figure(x_range=top_users['UserId'].tolist(), plot_height=400, plot_width=700, title="Top 20 users with Maximum numbers of reviews given",
               toolbar_location=None,y_range=(0, 500))
    p.vbar(x=top_users['UserId'].tolist(), top=top_users['Total_Reviews'].tolist(), width=0.5)
    p.line(top_users['UserId'].tolist(),top_users['Avg_Helpfulness_percentage'].tolist(),color='red',line_width=1)
    p.xaxis.major_label_orientation = "vertical"
    p.y_range.start = 0
    show(p)
    return render(request, 'adminPage.html',{'loader': revs})

def getPlot2(request):
    # top 20 most reviewed product
    review_df=k[2]
    top_products = review_df['ProductId'].value_counts().head(20).rename_axis('Product_Id').reset_index(name='Total Reviews')
    i1 = review_df.set_index('ProductId').index
    i2 = top_products.set_index('Product_Id').index
    top_products = pd.merge(top_products,
                            review_df[i1.isin(i2)].groupby('ProductId')['Score'].mean().rename_axis('Product_Id').reset_index(name='Avg_score'),
                            on="Product_Id")
    output_file("topProduct.html")
    p = figure(x_range=top_products['Product_Id'].tolist(), plot_height=400, plot_width=700, title="Top Reviewed products",
               toolbar_location=None,y_range=(0, 1000))

    p.vbar(x=top_products['Product_Id'].tolist(), top=top_products['Total Reviews'].tolist(), width=0.5)
    p.xaxis.major_label_orientation = "vertical"
    p.y_range.start = 0
    show(p)
    return render(request, 'adminPage.html',{'loader': revs})


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


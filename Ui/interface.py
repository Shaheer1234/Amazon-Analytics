from flask import Flask, render_template, request, url_for,redirect
import os
import numpy as np
import pygal as pg
import pandas as pd
from pygal.style import BlueStyle


def plot_dot(names,values,t,maint):
    dot_chart = pg.Dot(style=BlueStyle)
    dot_chart.title = maint
    dot_chart.x_labels = t
    for i in range(0,len(names)):
        dot_chart.add(names[i], values[i])      
    return dot_chart.render_data_uri()   

def plot_pie(names,values,t):
    graph = pg.Pie(style=BlueStyle)
    graph.title = t
    for i in range(0,len(names)):
        graph.add(names[i], values[i])
            
    return graph.render_data_uri()
def plot_bar(names,values,t,maint):
    graph = pg.Bar(show_y_labels=False,style=BlueStyle,height=340,width=800)
    graph.title = maint
    graph.x_labels = t
    for i in range(0,len(names)):
        graph.add(names[i], values[i])
            
    return graph.render_data_uri()
def plot_gauge(names,values,t,maint):
    gauge_chart = pg.Gauge(human_readable=True,style=BlueStyle,height=640)
    gauge_chart.title=maint
    gauge_chart.range = [0, 1000000]
    for i in range(0,len(names)):
        gauge_chart.add(names[i],np.sum(np.array(values[i])))
    
    return gauge_chart.render_data_uri()
def plot_dataframe():
    data = pd.read_csv('data.csv',)
    data = data.drop(['Unnamed: 0'],axis=1)
    cols =['Reviewer Username','Gender','Age Group','Product Type','Price(Dollar)']
    idata=data[cols].dropna()
    print idata
    index=np.random.choice(idata.shape[0], 10)
    indexed_df =idata.ix[index]
    line_chart = pg.Bar()
    line_chart.title = 'Samples From Scrapped Amazon Data'
    for c in cols:
        line_chart.add(c,indexed_df[c].tolist())
    return line_chart.render_table(style=True, total=False)

def plot_Life_expectation():
    data = pd.read_csv('Exp Life.csv')
    cols = ['2013; Female', '2013; Male']
    
    line_chart = pg.Bar(style=BlueStyle,human_readable=True,x_label_rotation=45,height=340,width=800,show_y_labels=False)
    line_chart.title = 'Life Expectation Across Age Groups'
    line_chart.x_labels = data['Age Group']
    for c in cols:
        line_chart.add(c, data[c].tolist())
        
    return line_chart.render_data_uri()

def plot_Death_Rate():
    data = pd.read_csv('Death Rate.csv')
    cols = ['2013; Female', '2013; Male']
    
    line_chart = pg.Line(style=BlueStyle,human_readable=True,x_label_rotation=45,show_y_labels=False)
    line_chart.title = 'Death Rate Age Groups'
    line_chart.x_labels = data['Age Group']
    for c in cols:
        line_chart.add(c, data[c].tolist())
        
    return line_chart.render_data_uri()


    
app = Flask(__name__)
def dataframeReader():
    data = pd.read_csv('data.csv',encoding='utf-8')
    data = data.drop(['Unnamed: 0'],axis=1)
    idata=data[['Reviewer Username','Gender','Age Group','Product Type','Price(Dollar)']]
    return idata

def getInformation(idata):
    females  = idata.where(idata['Gender']=='female').dropna()
    males = idata.where(idata['Gender']=='male').dropna()
    labels = ['Books','Electronics','Desktop','Others']
    values =[]
    values.append(males['Product Type'].value_counts().values)
    values.append(females['Product Type'].value_counts().values)
    titles = ['Male','Female']
    return titles,values,labels

def getInformationAge(idata):
    one  = idata.where(idata['Age Group']=='13-17').dropna()
    two = idata.where(idata['Age Group']=='17-33').dropna()
    three = idata.where(idata['Age Group']=='33-90').dropna()
    labels = ['Books','Electronics','Desktop','Others']
    values =[]
    values.append(one['Product Type'].value_counts().values)
    values.append(two['Product Type'].value_counts().values)
    values.append(three['Product Type'].value_counts().values)    
    titles = ['13-17','17-33','33-90']
    return titles,values,labels

def get_spendings_on_product(name,idata):
    females  = idata.where(idata['Gender']=='female').dropna()
    males = idata.where(idata['Gender']=='male').dropna()
    booksMale = males.where(males['Product Type']== name).dropna()
    booksfemale = females.where(females['Product Type']== name).dropna()

    spending_books_male =(booksMale['Price(Dollar)']+1).value_counts()
    spending_books_female =(booksfemale['Price(Dollar)']+1).value_counts()

    total_spending_books_male = np.sum((spending_books_male.keys()*spending_books_male.values).values)
    total_spending_books_female = np.sum((spending_books_female.keys()*spending_books_female.values).values)
    return total_spending_books_male,total_spending_books_female

def get_spendings_on_product_Age(name,idata,check):
    obj  = idata.where(idata['Age Group']==check).dropna()
    booksObj = obj.where(obj['Product Type']== name).dropna()

    spending_books_obj =(booksObj['Price(Dollar)']+1).value_counts()

    total_spending_books_obj = np.sum((spending_books_obj.keys()*spending_books_obj.values).values)
    return total_spending_books_obj

@app.route('/')
def pygalexample():
    try:

        d = dataframeReader()
        names,vs,t= getInformation(d)
        spendings_male = [ get_spendings_on_product(t,d)[0] for t in ['book','electronic','desktop','$0']]
        spendings_female = [ get_spendings_on_product(t,d)[1] for t in ['book','electronic','desktop','$0']]
        
        graph_data = plot_bar(names,vs,['Books','Electronics','Computer','Others'],'Gender Specific categorywise purchases')
        graph_data2 = plot_gauge(names,[spendings_male,spendings_female],[],'Total Revenue from Sales based on Gender')
        graph_data1 = plot_pie(['Male','Female'],[3720,2600],'')
        graph_data3 = plot_pie(['Age:13-17','Age:17-33','Age:33-90'],[200,5367,837],'')
        graph_data4 = plot_pie(['Books','Electronics','Computer','Others'],[2644,1923,1679,74],'')
        graph_data5 = plot_dot(names,[spendings_male,spendings_female],['Books','Electronics','Computer','Others'],'')
        paths = []
        titles = ['Gender Percentage in Amazon Reviews','Age Group Percentage in Amazon Reviews','Product Category Distribution','Revenue Generated Based on Product Category']
        paths.append(graph_data1)
        paths.append(graph_data3)
        paths.append(graph_data4)
        paths.append(graph_data5)
        return render_template("home.html", **locals())
    except Exception, e:
        return(str(e))


@app.route('/who')
def datavisualization():
    try:
        graph_data=plot_Life_expectation()
        d = dataframeReader()
        names,vs,t= getInformationAge(d)
        spendings_one = [ get_spendings_on_product_Age(t,d,'13-17') for t in ['book','electronic','desktop','$0']]
        spendings_two = [ get_spendings_on_product_Age(t,d,'17-33') for t in ['book','electronic','desktop','$0']]
        spendings_three = [ get_spendings_on_product_Age(t,d,'33-90') for t in ['book','electronic','desktop','$0']]
        graph_data5 = plot_dot(names,[spendings_one,spendings_two,spendings_three],['Books','Electronics','Computer','Others'],'')
        graph_data1 = plot_Death_Rate()
        paths =[]
        titles = ['Age Based Revenue Analysis','Death Rate']
        paths.append(graph_data5)
        paths.append(graph_data1)
        
        return render_template("home.html", **locals())
    except Exception, e:
        return(str(e))
    


if __name__ == '__main__':
    app.debug = True
    app.run()

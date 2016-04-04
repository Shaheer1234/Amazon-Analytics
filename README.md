# Amazon-Analytics

###User Interface 

Run Server using:
python interface.py
(will run at localhost:5000)

Dependencies:
- Flask
- pygal
- pandas python
- numpy 

Installation:

Pygal can be installed using <br />

pip install pygal <br />
-For further installation http://www.pygal.org/en/latest/installing.html <br /><br />


###Data Analysis

Data Analysis Notebooks are added in notebook folder.

Dependencies:

- Python
- Ipython Notebook
- scikit-learn
- Seaborn
- plotly (For Amazon Analysis ipython Notebook, it can be visualized using Amazon Analysis.html. In case of just visualizing no installation will be required)

Installation:

pip install -U scikit-learn <br />
For further installation details http://scikit-learn.org/stable/install.html <br /><br />
pip install seaborn <br />
For further installation details https://stanford.edu/~mwaskom/software/seaborn/installing.html <br /><br />
pip install plotly <br />
For Further installation details https://plot.ly/matplotlib/getting-started/<br /><br />

###Scrapping

Scraping of Amazon products and reviews is performed using Scrapy and sqlite is used as database to store data.

Dependencies:

- Scrapy
- sqlite

Installation:

sqlite<br />
Download precompilled binaries from: <br />
https://www.sqlite.org/download.html and add to operating system environment path vairables.<br /><br />

####Datasets

Blog Corpus <br />
This dataset is used to train Sentiment analysis model for Age and Gender Prediction of reviewers.<br />
Download if further or retraining of models is required. <br />
http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm  <br />

World Health Orginzation dataset for Age Group analytics (United States) <br />
Download to review(CSV File is added to dataset Folder) <br />
http://apps.who.int/gho/data/?theme=main&vid=61780





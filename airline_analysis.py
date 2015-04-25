													###############################
													## Airline Feedback Analysis ##
													###############################


##############
## Packages ##
##############
import nltk
import json
import glob
import string
import sqlite3
import argparse
import numpy as np
import codecs,re,time
from sklearn.svm import SVR
from sklearn.svm import NuSVC
from sklearn.svm import LinearSVC
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.metrics import classification_report

########################################
## command options & argument parsing ##
########################################

parser = argparse.ArgumentParser()  #creating ArgumentParser Object
parser.add_argument('--classifier', help="Choose the Classifier Algorithm to use.[NaiveBayes or SVM]") #specify Command-Line options
args = parser.parse_args()  #returns data from the argument specified
if args.classifier=='NaiveBayes':
    class_algo="NaiveBayes"
elif args.classifier=='SVM':
    class_algo="SVM"
else:
    print "error: Enter a Classifier."

####################################
## Loading the pre-processed data ##
####################################


X_test=[]
X_train=[]
y_train=[]

def tokenize(text):
    text = "".join([ch for ch in text if ch not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

tags = [] #labels

###########################
## Loading the test data ##
###########################
cmt_no=len(glob.glob('txt/cmt_0*.txt'))
for i in range(cmt_no):
	filename='txt/cmt_0%d.txt'%(i,)
	fp=open(filename,"r")
	file1=[json.loads(line) for line in codecs.open(filename,'r','utf8')]
	X_train.append(file1[0]['reviews'])
	if file1[0]['Recommended']=="yes":
		tags.append('pos')
	else:
		tags.append('neg')

tags1=[]
cmt_no1=len(glob.glob('cmt/cmt_0*.txt'))
for i in range(cmt_no1):
	filename='cmt/cmt_0%d.txt'%(i,)
	fp=open(filename,"r")
	file1=[json.loads(line) for line in codecs.open(filename,'r','utf8')]
	X_test.append(file1[0]['reviews'])
	if file1[0]['Recommended']=="yes":
		tags1.append('pos')
	else:
		tags1.append('neg')

#############################
## Training the Classifier ##
#############################
y_train=np.array(y_train)

if class_algo=="SVM":
	X_test=np.array(X_test)
	X_train=np.array(X_train)
	tags=np.array(tags)
	tags1=np.array(tags1)
	classifier = Pipeline([
        ('vectorizer', CountVectorizer(analyzer='word',tokenizer=tokenize,stop_words='english',binary=True)),
        ('tfidf', TfidfTransformer()),
        ('clf', OneVsOneClassifier(LinearSVC()))])
        classifier.fit(X_test[:], tags1[:])
        predicted = classifier.predict(X_train)

elif class_algo=="NaiveBayes":
 	word_vectorizer = CountVectorizer(analyzer='word',tokenizer=tokenize,stop_words='english',binary=True)
 	trainset = word_vectorizer.fit_transform(X_test)
 	mnb = MultinomialNB()
 	mnb.fit(trainset, tags1)
 	testset=word_vectorizer.transform(X_train)
 	predicted=mnb.predict(testset)
 	

conn=sqlite3.connect("test.db") #connecting to DB
conn.executescript('drop table if exists Airlines_Review')
conn.execute('''create table if not exists Airlines_Review(Customer_name varchar(30),Airline_name varchar(50),Catering int,Entertaintment int,Staff_service int,Seat_comfort int,Rating int,Money_val int,Recommended varchar(5),flag varchar(5),month varchar(40),pos_prob number(10,3),neg_prob number(10,3));''')
print '''################################
## Table created Successfully ##
################################'''
for i in range(cmt_no1):
	filename='cmt/cmt_0%d.txt'%(i,)
	fp=open(filename,"r")
	file1=[json.loads(line) for line in open(filename)]
	title=file1[0]['air_title']
	val_money=file1[0]['Value for money']
	mnth=file1[0]['month']
	seat=file1[0]['Seat Comfort']
	rcmd=file1[0]['Recommended']
	rating=file1[0]['Rating']
	staff=file1[0]['Staff Service']
	entmt=file1[0]['Entertainment']
	ctrng=file1[0]['Catering']
	cst_name=file1[0]['Customer_name']
	cst_name= string.replace(cst_name,"'","''")
	conn.execute("INSERT INTO Airlines_Review (Customer_name, Airline_name, Catering, Entertaintment, Staff_service, Seat_comfort, Rating, Money_val, Recommended, \
	 flag, month) VALUES ('"+cst_name+"','"+str(title)+"','"+str(ctrng)+"','"+str(entmt)+"','"+str(staff)+"','"+str(seat)+"','"+str(rating)+"','"+str(val_money)+"','"+str(rcmd)+"','"+str(predicted[i])+"','"+str(mnth)+"')");

conn.commit()

#####################################
## printing the DBtable on console ##
#####################################

cursor=conn.execute("select * from Airlines_Review")
for row in cursor:
   print row[0],"\t",row[2],"\t",row[1],"\t",row[3],"\t",row[4],"\t",row[5],"\t",row[6],"\t",row[7],"\t",row[8],"\t",row[9],"\t",row[10],"\n"
 
conn.close() #closing the db connection

######################
## Acccuracy Scores ##
######################

print "Classifier Accuracy:",accuracy_score(tags, predicted)*100,"%"
print classification_report(tags, predicted)

####################################################################################
####                            /* __Project_Lab__ */							####
#### __Project_Title__: Airline Feedback Analysis								####
#### __Domain__: NLP, Data Mining, Artificial Intelligence						####
#### __College__: College of Engineering, Guildy, Anna University				####
#### __Branch__: B.E Computer Science & Engineering								####
#### __Semester__: Six __Semester__                                             ####
#### __Technology_Used__: Python & Qlikview										####
#### __Done_by__: 1>Sree Harissh Venu (2012-103-072)							####
####		  	  2>Vignesh Mohan (2012-103-082)								####
#### __Date__: 25th March 2015													####
####																			####
####################################################################################

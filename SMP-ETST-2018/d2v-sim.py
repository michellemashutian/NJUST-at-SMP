# -*- coding:utf-8 -*-
#d2v_ap

from __future__ import division
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from gensim import corpora, models, similarities
from scipy.sparse import csr_matrix, coo_matrix
import pickle
import numpy as np
import logging
import MySQLdb as mdb
#import time
#import timeit
#import datetime
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def cos(x,y):
    dot_product=0.0
    A=0.0
    B=0.0
    for a,b in zip(x,y):
        dot_product+=a*b
        A+=a**2
        B+=b**2
    return (dot_product/((A*B)**0.5))


con=mdb.connect(host='localhost',user='root',passwd='123456',db='smp',charset='utf8')
cur=con.cursor()

sqli="select idx,sen_pro from candidate_sentence"
cur.execute(sqli)
result = cur.fetchall()

sqli1="select idx,sen_pro from original_sentence"
cur.execute(sqli1)
original = cur.fetchall()

all_text = []
for r in result:
    all_text.append(r[1].strip().split(" "))
for o in original:
    all_text.append(o[1].strip().split(" "))

count=0

doc=[]

sentences =[]
for i in range(len(all_text)):
    string = "DOC_" + str(i)
    sentence = models.doc2vec.LabeledSentence(all_text[i], labels = [string])
    sentences.append(sentence)

d2v = models.Doc2Vec(sentences, size = 100, window = 5, min_count = 0, dm = 1)

#Doc2Vec train
for j in range(5):
    d2v.train(sentences)
features=[]

for ii,term in enumerate(sentences):
    feature=[]
    string = "DOC_" + str(ii)
    for term in d2v[string]:
        feature.append(term)
    features.append(feature)

candidate_text = features[:1000]
original_text = features[1000:]

update = "update candidate_sentence set d2v_sim=%s where idx = %s"

for i in range(len(candidate_text)):
    similarity = []
    for j in range(len(original_text)):
        sim=cos(candidate_text[i],original_text[j])
        #print(sim)
        similarity.append(sim)
    index = similarity.index(max(similarity))
    print(i,index)
    cur.execute(update,(index+1,i+1))
        

cur.close()
con.commit()
con.close()

from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer
import MySQLdb as mdb
con=mdb.connect(host='localhost',user='root',passwd='123456',db='smp',charset='utf8')
cur=con.cursor()
sqli="select idx,sen_pro from candidate_sentence"
cur.execute(sqli)
result = cur.fetchall()
global count
count=0

def cos(x,y):
    dot_product=0.0
    A=0.0
    B=0.0
    for a,b in zip(x,y):
        dot_product+=a*b
        A+=a**2
        B+=b**2
    return (dot_product/((A*B)**0.5))


sqli1="select idx,sen_pro from original_sentence"
cur.execute(sqli1)
original = cur.fetchall()
original_text = []
for o in original:
    original_text.append(o[1])

for i in result:
    similarity = []
    vec=[]
    original_text.append(i[1])
    for k in range(len(original_text)):
        vec.append([])
    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(original_text))
    word=vectorizer.get_feature_names()
    weight=tfidf.toarray()
    for i in range(len(weight)):
        for j in range(len(word)):
            print(word[j],weight[i][j])
            
cur.close()
con.commit()
con.close()

import lda
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

all_text = []
for i in result:
    all_text.append(i[1])

all_text = []
for o in original:
    all_text.append(o[1])

update = "update candidate_sentence set lda_sim =%s where idx = %s"

vec = []
for k in range(len(all_text)):
    vec.append([])

corpus=CountVectorizer().fit_transform(all_text)
model = lda.LDA(n_topics=20, n_iter=2000, random_state=1)
model.fit(corpus)

for num,items in enumerate(model.doc_topic_):
    vec[num]=[item for item in items]

candidate_vec = vec[:1000]
original_vec = vec[1000:]

for i in range(len(candidate_vec)):
    similarity = []
    for j in range(len(original_vec)):
        sim=cos(candidate_vec[i],original_vec[j])
        similarity.append(sim)
    index = similarity.index(max(similarity))
    print(i,index)
    cur.execute(update,(index+1,i+1))

cur.close()
con.commit()
con.close()

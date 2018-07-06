# -*- encoding:gbk -*-
import MySQLdb as mdb
from nltk.tokenize import WordPunctTokenizer
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import Word2Vec


word_vectors = KeyedVectors.load_word2vec_format('C:\Users\IRTM\Desktop\代码\zhwiki_2017_03.sg_50d.word2vec',binary=False)

con=mdb.connect(host='127.0.0.1',user='root',passwd='123456',db='smp',charset='utf8')
cur=con.cursor()

def word2vec_sim(a,b):
    words1 = WordPunctTokenizer().tokenize(a)
    words2 = WordPunctTokenizer().tokenize(b)
    sim = 0.0
    for w1 in words1:
        for w2 in words2:
            try:
                sim = sim + word_vectors.similarity(w1,w2)
            except:
                sim = sim + 0.0
    if len(words1)==0 or len(words2)==0:
        return 0
    else:
        return sim/(len(words1)*len(words2))

sqli="select idx,sen_pro from candidate_sentence"
cur.execute(sqli)
result = cur.fetchall()

sqli1="select idx,sen_pro from original_sentence"
cur.execute(sqli1)
original = cur.fetchall()

all_text = []
for r in result:
    all_text.append(r[1].strip())
for o in original:
    all_text.append(o[1].strip())

candidate_text = all_text[:1000]
original_text = all_text[1000:]

update = "update candidate_sentence set w2v_sim = %s where idx = %s"
for i in candidate_text:
    similarity = []
    for j in original_text:
        similarity.append(word2vec_sim(i,j))
    index = similarity.index(max(similarity))
    print(candidate_text.index(i),index)
    cur.execute(update,(index+1,candidate_text.index(i)+1))


cur.close()
con.commit()
con.close()

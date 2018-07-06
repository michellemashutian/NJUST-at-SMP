#coding=utf-8
import MySQLdb as mdb
con=mdb.connect(host='localhost',user='root',passwd='123456',db='smp',charset='utf8')
cur=con.cursor()

def jaccard(p,q):
    c=[a for a in p if a in q]
    return(float(len(c))/(len(p)+len(q)-len(c)))

sqli="select idx,sen_pro from candidate_sentence"
cur.execute(sqli)
result = cur.fetchall()

sqli1="select idx,sen_pro from original_sentence"
cur.execute(sqli1)
original = cur.fetchall()

update = "update candidate_sentence set jaccard_sim=%s where idx = %s"
for i in range(len(result)):
    jacc = []
    for j in range(len(original)):
        jacc_sim=jaccard(result[i][1].split(" "),original[j][1].split(" "))
        jacc.append(jacc_sim)
    print(i,max(jacc))
    index = jacc.index(max(jacc))
    cur.execute(update,(index+1,i+1))

cur.close()
con.commit()
con.close()

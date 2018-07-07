import Levenshtein

with open('../B数据集.txt', encoding='utf-8') as f:
    a = []
    for i in f:
        i = i.strip().split('\t')
        a.append(i)

with open('../A数据集.txt', encoding='utf-8') as f:
    b = []
    for i in f:
        i = i.strip().split('\t')
        if len(i) == 2:
            b.append(i)


r = []
x = 0
for i in a:
    x += 1
    d = {}
    for j in b:
        m = Levenshtein.distance(i[1], j[1])
        s = 1-m/max([len(i[1]), len(j[1])])
        d[j[0]] = s
    c = sorted(d.items(), key=lambda e:e[1], reverse=True)
    r.append(i[0]+'\t'+c[0][0]+'\t'+str(c[0][1]))
    if x%10 == 0:
        print(x)

with open('r.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(r))

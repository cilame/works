import os

s = filter(lambda i:not i.endswith('py'),os.listdir('.'))

t = {}
for i in s:
    k = tuple(map(lambda j:int(j[:-4]),os.listdir(i)))
    t[k] = i

def get_name(g):
    for i in t:
        if g in i:
            return t[i]
    return None

for i in range(1,600):
    v = get_name(i)
    if v:
        print v

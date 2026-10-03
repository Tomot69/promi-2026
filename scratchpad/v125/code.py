import io,re,sys
a,b=int(sys.argv[1]),int(sys.argv[2])
L=io.open('app.html',encoding='utf-8').read().split('\n')[a-1:b]
S='\n'.join(L); S=re.sub(r'/\*.*?\*/','',S,flags=re.S)
for l in S.split('\n'):
    if l.strip(): print(l[:260])

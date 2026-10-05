import io,re
S=io.open('app.html',encoding='utf-8').read()
L=S.split('\n'); l=L[2518]; assert l.count('--p-corps-promi:#335382')==1
L[2518]=l.replace('--p-corps-promi:#335382','--p-corps-promi:#8ACBE8'); io.open('app.html','w',encoding='utf-8').write('\n'.join(L))
W=io.open('Promi+Design.swift',encoding='utf-8').read()
assert W.count('/// clair #CFE5FE · sombre #335382')==1; W=W.replace('/// clair #CFE5FE · sombre #335382','/// clair #CFE5FE · sombre #8ACBE8 (Tropical Breeze, Pantone 13-4307 TPG — Tom, 5 oct. 2026)')
io.open('Promi+Design.swift','w',encoding='utf-8').write(W)

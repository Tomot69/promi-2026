import io, sys
sys.path.insert(0,'scratchpad/v121'); from hunks import H, old_new
S=io.open('app.html',encoding='utf-8').read()
for i in [int(x) for x in sys.argv[1].split(',')]:
    o,n=old_new(H[i]); c=S.count(o)
    assert c==1, ('morceau %d trouvé %d fois' % (i,c))
    S=S.replace(o,n); print('morceau %d appliqué'%i)
io.open('app.html','w',encoding='utf-8').write(S)

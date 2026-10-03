import re, io, sys
D=io.open('scratchpad/v121/diff-v119.txt',encoding='utf-8').read().split('\n')
H=[]; cur=None
for n,l in enumerate(D,1):
    if l.startswith('@@'):
        cur={'deb':n,'lignes':[]}; H.append(cur); continue
    if cur is not None and (l[:1] in (' ','-','+')) and not l.startswith('+++') and not l.startswith('---'): cur['lignes'].append(l)
def old_new(h):
    o=[l[1:] for l in h['lignes'] if l[:1] in (' ','-')]; nw=[l[1:] for l in h['lignes'] if l[:1] in (' ','+')]; return '\n'.join(o),'\n'.join(nw)
if __name__=='__main__':
    for i,h in enumerate(H):
        ch=[l for l in h['lignes'] if l[:1] in '+-']
        print(i, h['deb'], len(ch), (ch[0][:110] if ch else ''))

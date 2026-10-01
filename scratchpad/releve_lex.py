import re,io,json,html
S=io.open('app.html',encoding='utf-8').read()
L=lambda p:S.count('\n',0,p)+1
TARGET=re.compile(r"Nu[ée]es?|NU[ÉE]ES?|nuées?|Cercle|CERCLE|(?<=\s)cercle\b")
def dec(s):
    s=re.sub(r"\\u([0-9a-fA-F]{4})",lambda m:chr(int(m.group(1),16)),s)
    s=re.sub(r"\\x([0-9a-fA-F]{2})",lambda m:chr(int(m.group(1),16)),s)
    return html.unescape(s)
comment=[]
for m in re.finditer(r"/\*.*?\*/|<!--.*?-->",S,re.S): comment.append((m.start(),m.end()))
import bisect
starts=[c[0] for c in comment]
def incom(p):
    i=bisect.bisect_right(starts,p)-1
    return i>=0 and comment[i][0]<=p<comment[i][1]
res=[]
for sm in re.finditer(r"<script[^>]*>(.*?)</script>",S,re.S):
    a=sm.start(1); body=sm.group(1)
    # remove // line comments positions
    lc=[(a+m.start(),a+m.end()) for m in re.finditer(r"(?<![:\\'\"=])//[^\n]*",body)]
    for m in re.finditer(r"'(?:[^'\\\n]|\\.)*'|\"(?:[^\"\\\n]|\\.)*\"|`(?:[^`\\]|\\.)*`",body):
        p=a+m.start()
        if incom(p) or any(x<=p<y for x,y in lc): continue
        raw=m.group(0); s=dec(raw[1:-1])
        if not TARGET.search(s): continue
        if re.fullmatch(r"[A-Za-z_$#.][A-Za-z0-9_$\-#. >:,\[\]=\"'*()]*",s) and s not in ('Cercle','CERCLE','Le Cercle','LE CERCLE'): continue
        res.append({'k':'js','l':L(p),'raw':raw[:300],'t':s[:300]})
H=re.sub(r"<script[^>]*>.*?</script>|<style[^>]*>.*?</style>|<!--.*?-->",lambda m:re.sub(r"[^\n]",' ',m.group(0)),S,flags=re.S)
for m in re.finditer(r">([^<]+)<",H):
    s=html.unescape(m.group(1))
    if TARGET.search(s) and s.strip(): res.append({'k':'html','l':L(m.start()),'raw':m.group(1)[:300],'t':s.strip()[:300]})
for m in re.finditer(r"(aria-label|title|placeholder|alt|data-label|data-t)=\"([^\"]*)\"",H):
    s=html.unescape(m.group(2))
    if TARGET.search(s): res.append({'k':'attr','l':L(m.start()),'raw':m.group(0)[:300],'t':s})
json.dump(res,open('scratchpad/lex.json','w'),ensure_ascii=False,indent=1)
print(len(res))
for r in res: print(r['k'],r['l'],'|',r['t'][:170].replace('\n',' '))

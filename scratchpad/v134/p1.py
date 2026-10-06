import io,re
S=io.open('app.html',encoding='utf-8').read()
def r(a,b,n=1):
    global S
    assert S.count(a)==n,(a[:60],S.count(a)); S=S.replace(a,b)
r("--c-cobalt50:#1A52F0;--c-lilas85:#E8DAFF;","--c-cobalt50:#0E78F2;--c-lilas85:#F4EEFF;")
print(S.count('#FF9F84'), S.count('--p-corps-promi:#1A52F0'), S.count('#1A52F0'))
S=S.replace('--c-orange-maparole-cobalt:#FF9F84','--c-orange-maparole-cobalt:#FED0C3').replace('--p-corps-promi:#1A52F0','--p-corps-promi:#0E78F2')
i=S.index('<script id="lot-V133-BLEU">'); j=S.index('</script>',i)+9
S=S[:i]+'''<script id="lot-V133-BLEU">
/* ⚑ v134 (Tom, 6 oct. 2026, C-050) — LE BLEU DU CORPS SOMBRE D'UN PROMI EST DÉFINITIF : #0E78F2, « choisi en connaissance de cause ».
   Le paramètre ?bleu= de v133 est RETIRÉ. Il ne reste ici que la lecture du jeton, dont le mur a besoin pour savoir qu'il est posé sur ce corps. */
(function(){ var R=document.documentElement;
  window._bleuPromi=function(){ var s=String(getComputedStyle(R).getPropertyValue('--c-cobalt50')||'').trim(), m=/^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(s);
    return m ? [parseInt(m[1],16),parseInt(m[2],16),parseInt(m[3],16)] : [14,120,242]; }; })();
</script>'''+S[j:]
r("(window._bleuPromi?window._bleuPromi():[26,82,240])","(window._bleuPromi?window._bleuPromi():[14,120,242])")
io.open('app.html','w',encoding='utf-8').write(S)
for f,subs in (('PROMI-TOKENS.json',[('"sombre": "#1A52F0"','"sombre": "#0E78F2"'),('"--c-orange-maparole-cobalt": "#FF9F84"','"--c-orange-maparole-cobalt": "#FED0C3"'),('"--c-cobalt50": "#1A52F0"','"--c-cobalt50": "#0E78F2"'),('"--c-lilas85": "#E8DAFF"','"--c-lilas85": "#F4EEFF"')]),):
    T=io.open(f,encoding='utf-8').read()
    for a,b in subs: assert T.count(a)==1,a; T=T.replace(a,b)
    io.open(f,'w',encoding='utf-8').write(T)

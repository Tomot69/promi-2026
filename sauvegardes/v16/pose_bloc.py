# Pose (ou repose) le bloc lot-V16 avant </body>, avec l'OFL et le texte « À propos » de Tom.
import io, json, re
F='app.html'; S=io.open(F,encoding='utf-8').read()
B=io.open('sauvegardes/v16/bloc_v16.html',encoding='utf-8').read()
corps=io.open('sauvegardes/v16/OFL-1.1.txt',encoding='utf-8').read()
i=corps.index('-----------------------------------------------------------\nSIL OPEN FONT LICENSE')
OFL=("Copyright © 2020, 2024 Braille Institute of America, Inc., with Reserved Font Names "
     "Atkinson and Hyperlegible.\n\nThis Font Software is licensed under the SIL Open Font License, Version 1.1.\n"
     "This license is copied below, and is also available with a FAQ at:\nhttps://openfontlicense.org\n\n\n")+corps[i:]
AP=io.open('sauvegardes/v16/apropos.html',encoding='utf-8').read().strip()
B=B.replace('__OFL__', json.dumps(OFL,ensure_ascii=False)).replace('__APROPOS__', json.dumps(AP,ensure_ascii=False))
# retire l'ancienne pose
S=re.sub(r'<style id="lot-V16-css">.*?</style>\n<script id="lot-V16">.*?</script>\n', '', S, flags=re.S)
n=S.count('</body>'); assert n>=1
k=S.rindex('</body>'); S=S[:k]+B.rstrip()+'\n'+S[k:]
io.open(F,'w',encoding='utf-8').write(S); print('posé', len(B))

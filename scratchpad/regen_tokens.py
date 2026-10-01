#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RÉGÉNÈRE PROMI-TOKENS.json DEPUIS LE BLOC DU JEU DE app-identite.html.
   Le bloc CSS est devenu la vérité pendant le chantier : on le relit, on reconstruit le JSON,
   et le Swift se régénère depuis le JSON. L'ordre du §3 est respecté — le JSON est la source,
   mais ici c'est lui qu'on rattrape, une fois, en le disant."""
import io, re, json, datetime
SRC='app-identite.html'
S=io.open(SRC,encoding='utf-8').read()
i=S.find('<style id="lot-TOKENS-css">'); j=S.find('</style>',i)
assert i>0 and j>i
bloc=S[i:j]
# la palette FIXE, dans l'ordre où le bloc la donne
racine=re.search(r':root\{(.*?)\}', bloc, re.S).group(1)
fixe={}
for m in re.finditer(r'(--c-[a-z0-9-]+):(#[0-9A-Fa-f]{6})', racine):
    fixe[m.group(1)]=m.group(2).upper()
# les rôles : sombre au :root, clair sur .light
som=dict(re.findall(r'(--p-[a-z0-9-]+):(#[0-9A-Fa-f]{6})', racine))
cl_bloc=re.search(r'#device\.light[^{]*\{(.*?)\}', bloc, re.S).group(1)
cla=dict(re.findall(r'(--p-[a-z0-9-]+):(#[0-9A-Fa-f]{6})', cl_bloc))
roles={}
for k in som:
    n=k[4:]
    roles[n]={'clair':cla.get(k,som[k]).upper(),'sombre':som[k].upper()}
J=json.load(io.open('PROMI-TOKENS.json',encoding='utf-8'))
avant_fixe=len(J['palette_fixe']); avant_roles=len(J['roles'])
J['genere_le']=datetime.date.today().isoformat()
J['note']=("Source unique du design de Promi. Les rôles basculent avec le mode ; la palette fixe "
           "ne bascule jamais. ⚠ Les jetons `-txt` sont l'exception qui confirme la règle : ils "
           "portent l'ENCRE d'une nature ou d'un état, et celle-ci bascule (sombre = le pastel, "
           "clair = le compagnon sombre). Une règle qui peint du TEXTE les emploie ; une règle qui "
           "peint un APLAT emploie la valeur fixe.")
J['palette_fixe']=dict(sorted(fixe.items(), key=lambda kv: kv[1]))
J['roles']=roles
io.open('PROMI-TOKENS.json','w',encoding='utf-8').write(json.dumps(J,ensure_ascii=False,indent=2)+'\n')
print(f"palette fixe : {avant_fixe} → {len(fixe)}   ·   rôles : {avant_roles} → {len(roles)}")
neufs=[k for k in fixe if k not in json.load(io.open('sauvegardes/PROMI-TOKENS-avant-identite.json',encoding='utf-8'))['palette_fixe']] if __import__('os').path.exists('sauvegardes/PROMI-TOKENS-avant-identite.json') else []
if neufs: print('jetons neufs :', ', '.join(sorted(neufs)))

import io, ast
S=io.open('redteam_murs.py',encoding='utf-8').read()
i=S.index("PHRASES = ['Eh non"); j=S.index("res = []")
NEUF='''# ⚑ v133 (Tom, 6 oct. 2026) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_murs-avant-v133.py) : les phrases des murs sont réécrites par
#   Tom — DIX-HUIT, mot pour mot, dans cet ordre ; dans chacune, SEULS les mots listés prennent l'orange de Ma Parole ! ; le point
#   d'exclamation n'apparaît que dans « Ma Parole ! ». Espaces insécables avant « ! » et « ? ».
N = '\\u00a0'
TEXTES = [('Eh non. Mais avec ' + MP + ', oui.', [MP]), ('La solution commence par Ma et finit par Parole' + N + '!', ['Ma', 'Parole' + N + '!']),
    ('Toujours non. ' + MP + ', toujours oui.', [MP, 'oui']), ('Je vois bien que ça te titille. ' + MP + ' aussi.', [MP]),
    ('Tiens tiens, on dirait que ça commence à t’intéresser…', []), ('Tiens tiens. Vous ici.', []), ('Tu sais où trouver ' + MP + ' maintenant.', [MP]),
    ('On maintient cette position officielle, alors' + N + '?', ['officielle']), ('Allons bon. Nous y voilà à nouveau.', []),
    ('Entre nous, le mystère s’amenuise.', ['mystère']), ('Les pourparlers se prolongent, je vois.', ['pourparlers']),
    ('Tu peux continuer. Je tiens le registre.', ['registre']), ('Ici, tout restera entre nous.', []), ('Je commence à soupçonner une stratégie.', ['stratégie']),
    ('On pourrait presque en faire une tradition.', ['tradition']), ('Regarde-nous, avec nos petites habitudes.', ['habitudes']),
    ('Dis donc, tu viendrais presque pour moi.', ['moi']), ('On se retrouve ici tout à l’heure' + N + '?', [])]
PHRASES = [x[0] for x in TEXTES]; DER = len(PHRASES) - 1
'''
S=S[:i]+NEUF+S[j:]
def r(a,b,n=1):
    global S
    assert S.count(a)==n,(a,S.count(a)); S=S.replace(a,b)
r("JSON.stringify({n:20,t:Date.now(),der:19,decouvert:1})","JSON.stringify({n:%d,t:Date.now(),der:%d,decouvert:1})\" % (DER, DER - 1))".replace('"))','"))') if False else "JSON.stringify({n:17,t:Date.now(),der:16,decouvert:1})")
r("PHRASES[20]","PHRASES[DER]",2)
r("'5a · la 21e touche fait monter la 21e phrase'","'5a · la 18e touche fait monter la 18e phrase'")
r("MUR_ORANGE = 'rgb(255, 134, 100)' if th != 'light'","MUR_ORANGE = 'rgb(255, 159, 132)' if th != 'light'")
# contrôle neuf : les mots en orange, phrase par phrase
a="        t('5b · au-delà"
k=S.index(a); k2=S.index('\n',k)+1
AJ='''        # 9 (v133) · chaque phrase, mot pour mot, et SES mots en orange — eux seuls
        faux = []
        for i, (ph, mots) in enumerate(TEXTES):
            pg.evaluate("(i)=>localStorage.setItem('promi_murs',JSON.stringify({n:i,t:Date.now(),der:i-1,decouvert:1}))", i)
            pg.touchscreen.tap(*a); pg.wait_for_timeout(300)
            v = pg.evaluate("""()=>{const p=document.getElementById('murPhrase'); if(!p) return null; const base=getComputedStyle(p).color;
              return {texte:p.textContent, mp:[...p.querySelectorAll('.mp')].map(m=>m.textContent), cmp:[...p.querySelectorAll('.mp')].map(m=>getComputedStyle(m).color), base:base,
                autres:[...p.querySelectorAll('*')].filter(e=>!e.closest('.mp')&&e.childElementCount===0&&getComputedStyle(e).color!==base).length}}""")
            pg.evaluate("()=>{window._murBaisse&&_murBaisse()}"); pg.wait_for_timeout(120)
            if not v or v['texte'] != ph or v['mp'] != mots or any(c == v['base'] for c in v['cmp']) or len(set(v['cmp'])) > 1 or v['autres']:
                faux.append('%d %r → %r' % (i + 1, (v or {}).get('texte'), (v or {}).get('mp')))
        excl = [x for x in PHRASES if x.replace('Ma Parole' + N + '!', '').replace('Parole' + N + '!', '').count('!')]
        t('9 · les dix-huit phrases mot pour mot ; dans chacune, seuls les mots décidés sont en orange ; « ! » seulement dans « Ma Parole ! »', not faux and not excl and len(PHRASES) == 18, ' | '.join(faux[:3]) or '18 phrases, %d avec un mot en orange' % sum(1 for x in TEXTES if x[1]))
'''
S=S[:k2]+AJ+S[k2:]
S=S.replace("5 · les 21 phrases dans l'ordre, EN DUR ci-dessous (la 21e à la 21e touche)","5 · les 18 phrases (v133) dans l'ordre, EN DUR ci-dessous (la 18e à la 18e touche)")
ast.parse(S); io.open('redteam_murs.py','w',encoding='utf-8').write(S)

M=io.open('redteam_maparole.py',encoding='utf-8').read()
def m(a,b,n=1):
    global M
    assert M.count(a)==n,(a,M.count(a)); M=M.replace(a,b)
m("ORANGE = ('rgb(251, 76, 13)', 'rgb(255, 122, 85)', 'rgb(255, 134, 100)')","""ORANGE = ('rgb(251, 76, 13)', 'rgb(255, 122, 85)', 'rgb(255, 159, 132)')
# ⚑ v133 (Tom, 6 oct. 2026) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_maparole-avant-v133.py) : ① le corps sombre d'un Promi passe
#   à #1A52F0 (provisoire, C-050) : l'orange éclairci à 3:1 y est #FF9F84 (il remplace #FF8664) ; ② « le juge de l'orange accepte désormais
#   les mots listés, et seulement eux, dans les phrases des murs » — la liste est EN DUR ci-dessous (MOTS).
NB = '\\u00a0'; MPX = 'Ma Parole' + NB + '!'
MOTS = [[MPX], ['Ma', 'Parole' + NB + '!'], [MPX, 'oui'], [MPX], [], [], [MPX], ['officielle'], [], ['mystère'], ['pourparlers'], ['registre'], [], ['stratégie'], ['tradition'], ['habitudes'], ['moi'], []]""")
m("r'#(?:FB4C0D|FF7A55|FF8664)\\b|\\b251\\s*,\\s*76\\s*,\\s*13\\b|\\b255\\s*,\\s*122\\s*,\\s*85\\b|\\b255\\s*,\\s*134\\s*,\\s*100\\b'","r'#(?:FB4C0D|FF7A55|FF9F84)\\b|\\b251\\s*,\\s*76\\s*,\\s*13\\b|\\b255\\s*,\\s*122\\s*,\\s*85\\b|\\b255\\s*,\\s*159\\s*,\\s*132\\b'")
m("#(FB4C0D|FF7A55|FF8664)'","#(FB4C0D|FF7A55|FF9F84)'")
m("'#FF8664 (corps cobalt d\\'un Promi)'","'#FF9F84 (corps bleu d\\'un Promi)'")
a="        t('[%s] aucune erreur de page' % th"
AJ='''        # D (v133) · dans les dix-huit phrases, l'orange ne porte que les mots décidés
        pg.evaluate("()=>{window._murBaisse&&_murBaisse()}"); faux = []
        for i, mots in enumerate(MOTS):
            pg.evaluate("(i)=>localStorage.setItem('promi_murs',JSON.stringify({n:i,t:Date.now(),der:i-1,decouvert:1}))", i)
            if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(320)
            v = pg.evaluate("""(OR)=>{const p=document.getElementById('murPhrase'); if(!p||!p.classList.contains('leve')) return null; const out=[];
              const w=document.createTreeWalker(p,NodeFilter.SHOW_TEXT); let n; while(n=w.nextNode()){ if(n.nodeValue&&OR.indexOf(getComputedStyle(n.parentElement).color)>=0) out.push(n.nodeValue); } return out}""", list(ORANGE))
            pg.evaluate("()=>{window._murBaisse&&_murBaisse()}"); pg.wait_for_timeout(120)
            if v != mots: faux.append('%d → %r (décidé %r)' % (i + 1, v, mots))
        t('D · [%s] dans les dix-huit phrases, seuls les mots décidés portent l\\'orange' % th, not faux, ' | '.join(faux[:3]))
'''
assert M.count(a)==1; M=M.replace(a,AJ+a)
ast.parse(M); io.open('redteam_maparole.py','w',encoding='utf-8').write(M)

#!/usr/bin/env python3
"""v145 (C-112) — bâtir une Toile REMPLIE comme celle de Tom : 10, 25, 50 paroles plantées par l'app elle-même (le +, la nature, le bouton),
puis tout le stockage local gardé dans scratchpad/v145/etats/etat-N.json (relu ensuite comme sur un téléphone : à l'ouverture)."""
import sys, json, io, os; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
TITRES = ['rendre le livre', 'écrire à Lou', 'arroser le ficus', 'courir dimanche', 'appeler mamie', 'finir la maquette', 'ranger le garage', 'faire les crêpes',
          'réparer le vélo', 'trier les photos', 'apprendre la chanson', 'planter un arbre', 'passer voir Nico', 'envoyer la carte', 'dormir tôt', 'cuisiner pour Rachel',
          'lire le roman', 'nager jeudi', 'peindre la porte', 'répondre à Marion', 'aller au marché', 'vider la cave', 'préparer le voyage', 'payer Adrien',
          'tailler le rosier']
QUI = ['moi', 'moi', 'Rachel', 'moi', 'Marion', 'moi', 'Nico', 'moi', 'Adrien', 'moi']
def plante(pg, titre, qui, nature):
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(450)
    pg.evaluate("n=>{const x=[...document.querySelectorAll('#createSheet .tile')][n];x&&x.click()}", nature); pg.wait_for_timeout(1100)
    pg.evaluate("a=>{document.getElementById('fTitle').value=a[0];document.getElementById('fWho').value=a[1];window._csEnLair=true;window._csDueISO=null}", [titre, qui])
    pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(350)
os.makedirs('scratchpad/v145/etats2', exist_ok=True)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx)
    for i in range(50):
        t = TITRES[i % len(TITRES)] + ('' if i < len(TITRES) else ' encore')
        nat = 1 if i % 5 == 3 else 0
        B.plante_doigt(pg, t, QUI[i % len(QUI)], nat, attente=1700)
        if i % 6 == 2:   # une parole sur six est TENUE, par le bouton que le geste actionne (l'instant « tenu » joue en entier)
            pg.evaluate("()=>{ openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(1500)
            pg.evaluate("()=>{ var b=document.querySelector('#segStatus button[data-st=\"tenu\"]'); b&&b.click(); }"); pg.wait_for_timeout(3300)
            pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500)
        n = pg.evaluate("()=>promises.filter(p=>!p.draft).length")
        der = pg.evaluate("()=>{ var p=promises[promises.length-1]; return [p.title, !!p.chiche]; }")
        if der[1] != bool(nat): print('   ⚠ nature :', i, der, 'demandée', nat, flush=True)
        if (i + 1) in (10, 25, 50):
            pg.wait_for_timeout(2500); pg.evaluate("()=>{ try{saveState()}catch(e){} }"); pg.wait_for_timeout(300)
            st = pg.evaluate("()=>{ var o={}; for(var i=0;i<localStorage.length;i++){ var k=localStorage.key(i); o[k]=localStorage.getItem(k); } return o; }")
            io.open('scratchpad/v145/etats2/etat-%d.json' % (i + 1), 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False))
            B.capture(pg, 'scratchpad/v145/etats2/etat-%d.png' % (i + 1))
            print(i + 1, 'paroles plantées ; dans promises :', n, '; clés :', sorted(st.keys()), flush=True)
    print('erreurs', pg.erreurs[:3]); b.close()

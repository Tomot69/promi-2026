# -*- coding: utf-8 -*-
"""L'AIR ENTRE LES TEXTES — ce que le cran a mangé.

   Monter une taille sans reprendre les écarts resserre l'air PARTOUT où la cote suivante
   était calculée pour l'ancienne taille. On ne le voit pas dans un relevé de positions :
   les tops n'ont pas bougé, c'est la HAUTEUR des blocs qui a grandi vers le bas.

   On mesure donc l'ESPACE RÉEL — bas du bloc A → haut du bloc B — entre deux textes qui se
   recouvrent horizontalement, sur chaque écran, dans les deux thèmes ; et on compare la
   version d'aujourd'hui à la MÊME version dont on n'a remis que les quatre tailles à
   l'avant-cran. Tout le reste est identique — même jeu de démonstration, mêmes cotes :
   l'écart mesuré est donc exactement ce que le cran a coûté.
"""
import sys, json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8752/"
ECRANS = [
 ('fiche tenue',   "()=>{closeAll(); const p=promises.filter(q=>q.title==='planter un arbre')[0]; if(p)openDetail(p.id);}"),
 ('fiche à tenir', "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p)openDetail(p.id);}"),
 ('fiche en cours',"()=>{closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; if(p)openDetail(p.id);}"),
 ('fiche chiche',  "()=>{closeAll(); const p=promises.filter(q=>q.title==='le grand plongeoir')[0]; if(p)openDetail(p.id);}"),
 ('chiche lancé',  "()=>{closeAll(); const p=promises.filter(q=>q.title==='courir dimanche')[0]; if(p)openDetail(p.id);}"),
 ('gardé de côté', "()=>{closeAll(); const p=promises.filter(q=>q.draft)[0]; if(p)openDetail(p.id);}"),
 ('page +',        "()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"),
 ('Peaufiner',     "()=>{closeAll(); const p=promises.filter(q=>!q.draft)[0]; openDetail(p.id); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 ('Index 2',       "()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"),
 ('Index 3',       "()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=true; if(window._s4Index)_s4Index();}"),
 ('Fil',           "()=>{closeAll(); setView('fil');}"),
 ('Nuée',          "()=>{closeAll(); openEssaim('potager');}"),
 ('Nuée vide',     "()=>{closeAll(); openEssaim('atelier');}"),
 ('Peaufiner Nuée',"()=>{closeAll(); openEssaim('potager'); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 ("l'instant arrive",  "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('arrive');}catch(e){}},900);}}"),
 ("l'instant referme", "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('referme');}catch(e){}},900);}}"),
 ("l'instant après",   "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('apres');}catch(e){}},900);}}"),
 ('Réglages',      "()=>{closeAll(); document.getElementById('settingsBtn').click();}"),
]

# Un « bloc de texte » : une feuille qui porte des mots. On ne prend que la feuille du dessus
# (sinon on mesurerait un conteneur contre son propre enfant), et on ignore ce qui est trop
# petit pour être lu.
MESURE = r"""()=>{
  const dev=document.getElementById('device').getBoundingClientRect(), sc=dev.width/390;
  const EN_LIGNE = ['B','I','EM','STRONG','SPAN','SMALL','BR','U','A','CODE','SUP','SUB'];
  const bl=[];
  document.querySelectorAll('#device *').forEach(e=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return;
    const t=(e.textContent||'').trim(); if(!t) return;
    /* la feuille du dessus : aucun enfant de bloc porteur de texte */
    for(const k of e.children){ if(!EN_LIGNE.includes(k.tagName) && (k.textContent||'').trim()) return; }
    const r=e.getBoundingClientRect();
    const x=(r.x-dev.x)/sc, y=(r.y-dev.y)/sc, w=r.width/sc, h=r.height/sc;
    if(w<12||h<6||y<-40||y>884) return;
    bl.push({cle:(e.id? '#'+e.id : '.'+(''+e.className).split(' ').filter(Boolean).slice(0,2).join('.')),
             mot:t.slice(0,22), x:+x.toFixed(1), y:+y.toFixed(1), w:+w.toFixed(1), h:+h.toFixed(1),
             fs:parseFloat(c.fontSize)});
  });
  bl.sort((a,b)=>a.y-b.y);
  /* l'écart : bas de A → haut de B, pour deux blocs qui se recouvrent horizontalement.
     On garde, pour chaque bloc, son voisin du dessous le plus proche. */
  const paires=[];
  for(let i=0;i<bl.length;i++){
    let best=null;
    for(let j=0;j<bl.length;j++){
      if(i===j) continue;
      const a=bl[i], b=bl[j];
      if(b.y < a.y + a.h - 0.5) continue;                       /* B doit être SOUS A */
      const rec=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x);
      if(rec < Math.min(a.w,b.w)*0.34) continue;                /* et le recouvrir vraiment */
      const g=b.y-(a.y+a.h);
      if(!best || g<best.g) best={g:+g.toFixed(1), b:b};
    }
    if(best && best.g < 200)
      paires.push({a:bl[i].cle+' « '+bl[i].mot+' »', b:best.b.cle+' « '+best.b.mot+' »',
                   ecart:best.g, fs:Math.max(bl[i].fs,best.b.fs)});
  }
  return paires;
}"""

def releve(pg, js):
    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
    try: pg.evaluate(js)
    except Exception: pass
    pg.wait_for_timeout(2000)
    prec, stable = None, 0
    for _ in range(20):
        pg.wait_for_timeout(250)
        n = pg.evaluate("()=>[...document.querySelectorAll('#device *')]"
                        ".filter(e=>{const r=e.getBoundingClientRect();return r.width>4&&r.height>4;}).length")
        stable = stable + 1 if n == prec else 0
        prec = n
        if stable >= 2: break
    pg.wait_for_timeout(250)
    return pg.evaluate(MESURE)

def passe(fichier):
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
        pg.goto(BASE+fichier); pg.wait_for_timeout(6800)
        pg.evaluate('()=>{var o=document.getElementById("promiOnb");'
                    'if(o){o.classList.add("gone");o.style.display="none";}}')
        for th in ('dark','light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            for nom, js in ECRANS:
                out['%s [%s]' % (nom, th)] = releve(pg, js)
        b.close()
    return out

if __name__ == '__main__':
    quoi = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
    sortie = sys.argv[2] if len(sys.argv) > 2 else 'scratchpad/ecarts.json'
    r = passe(quoi)
    open(sortie,'w').write(json.dumps(r, ensure_ascii=False))
    print('%s → %s  (%d écrans, %d paires)'
          % (quoi, sortie, len(r), sum(len(v) for v in r.values())))

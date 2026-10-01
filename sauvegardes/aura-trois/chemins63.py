# CHANTIER 63 — LES CHEMINS VERS LA FICHE D'UNE PERSONNE, AU DOIGT. Chaque nom écrit dans une ligne est touché au centre
# de SON mot (rectangle du mot, pas de la ligne) sur un écran rouvert à neuf ; on attend la fiche refaite de CETTE personne
# (#personSheet.show et #psCadre[data-fiche=nom]). Et l'inverse : « +3 » n'ouvre personne, un glissement n'ouvre rien, et
# la rangée « À QUI » du Peaufiner d'un Promi RESTE un réglage (elle ne navigue pas).
# Doit ROUGIR sur l'app sans lot-CHEMINS-PERSONNE (la version fautive), puis passer.
import sys
from playwright.sync_api import sync_playwright
APP = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
PEAUF = "()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"
BASE = "()=>{ closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"
ECRANS = {
  'fiche de Nuée (potager)':        [(BASE, 200), ("()=>openEssaim('potager')", 1600)],
  'Peaufiner de la Nuée':           [(BASE, 200), ("()=>openEssaim('potager')", 1400), (PEAUF, 1400)],
  'fiche du Chiche « courir dimanche »': [(BASE, 200), ("()=>openDetail(127)", 1500)],
  'fiche du Promi « faire les crêpes »': [(BASE, 200), ("()=>openDetail(126)", 1500)],
  'Peaufiner du Promi (rangée À QUI)':   [(BASE, 200), ("()=>openDetail(126)", 1200), (PEAUF, 1400)],
}
# les mots à toucher, dans l'hôte : [sélecteur, mot, personne attendue (None = n'ouvre personne)]
CAS = {
  'fiche de Nuée (potager)':        [('#dptQui', 'Rachel', 'Rachel'), ('#dptQui', 'Adrien', 'Adrien'), ('#dptQui', '+3', None)],
  'Peaufiner de la Nuée':           [('.np-val', 'Rachel', 'Rachel'), ('.np-val', 'Adrien', 'Adrien'), ('.np-val', '+3', None)],
  'fiche du Chiche « courir dimanche »': [('#dptQui', 'Marion', 'Marion'), ('#dptQui', 'Rachel', 'Rachel')],
  'fiche du Promi « faire les crêpes »': [('#dptQui', 'Rachel', 'Rachel')],
  'Peaufiner du Promi (rangée À QUI)':   [('.s2-val', 'Rachel', None)],
}
MOT = r"""([sel, mot])=>{ const hs=[...document.querySelectorAll(sel)].filter(h=>h.getBoundingClientRect().height>0 && h.textContent.indexOf(mot)>=0);
  for(const h of hs){ const w=document.createTreeWalker(h, NodeFilter.SHOW_TEXT); let n;
    while((n=w.nextNode())){ const k=n.textContent.indexOf(mot); if(k<0) continue; const r=document.createRange(); r.setStart(n,k); r.setEnd(n,k+mot.length);
      const b=r.getBoundingClientRect(); if(b.width<=0) continue; const x=b.left+b.width/2, y=b.top+b.height/2, e=document.elementFromPoint(x,y);
      if(e && (h===e || h.contains(e))) return {x, y, texte:h.textContent.trim().slice(0,60)}; } }
  return null; }"""
ETAT = "()=>({fiche:document.getElementById('personSheet').classList.contains('show') ? (document.getElementById('psCadre')||{getAttribute:()=>'(ancienne)'}).getAttribute('data-fiche') : null})"
R = []
def t(nom, ok, d=''): R.append((nom, bool(ok), d)); print('%s  %s  %s' % ('OK  ' if ok else 'RATÉ', nom, d))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    err = []; pg.on('pageerror', lambda e: err.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    sc = pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().width/390")
    def ouvre(ec):
        for js, w in ECRANS[ec]: pg.evaluate(js); pg.wait_for_timeout(w)
    for ec, cas in CAS.items():
        for sel, mot, attendu in cas:
            ouvre(ec); m = pg.evaluate(MOT, [sel, mot])
            if not m: t('%s · « %s » visible et touchable' % (ec, mot), False, 'introuvable'); continue
            pg.mouse.click(m['x'], m['y']); pg.wait_for_timeout(1500); e = pg.evaluate(ETAT)
            if attendu: t('%s · toucher « %s » ouvre SA fiche (la refaite)' % (ec, mot), e['fiche'] == attendu, 'ligne « %s » → %s' % (m['texte'], e['fiche']))
            else:       t('%s · toucher « %s » n\'ouvre aucune personne' % (ec, mot), not e['fiche'], 'ligne « %s » → %s' % (m['texte'], e['fiche']))
    # un glissement sur un nom n'ouvre rien
    ouvre('fiche de Nuée (potager)'); m = pg.evaluate(MOT, ['#dptQui', 'Rachel'])
    if m:
        pg.mouse.move(m['x'], m['y']); pg.mouse.down(); pg.mouse.move(m['x'] + 30 * sc, m['y'], steps=6); pg.mouse.up(); pg.wait_for_timeout(900)
        e = pg.evaluate(ETAT); t('fiche de Nuée · un glissement de 30 pt sur « Rachel » n\'ouvre rien', not e['fiche'], str(e))
    t('aucune erreur de page', not err, str(err[:2]))
    b.close()
rates = [r for r in R if not r[1]]
print('\n%s' % ('✅  %d / %d' % (len(R), len(R)) if not rates else '❌  %d RATÉ(S) sur %d' % (len(rates), len(R))))
sys.exit(1 if rates else 0)

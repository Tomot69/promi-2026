# Audit de la fiche de la personne — les VARIANTES (rien n'est modifié dans app.html ; une page neuve par cas) :
#  · qui la fiche peut montrer (les prénoms de la rangée de l'Aura), « moi », un prénom sans aucun Promi
#  · le Cercle : #device.premium — les nœuds « prem-only » et le second anneau paraissent-ils ? (la fiche vit sous .frame)
#  · l'entrée depuis une fiche (.kring[data-p]) ouvre-t-elle la fiche de la personne ?
import sys, os, json
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
VIS = r"""()=>{ const sh=document.getElementById('personSheet'), q=(s)=>[...sh.querySelectorAll(s)];
  const vu=(e)=>{ const c=getComputedStyle(e), r=e.getBoundingClientRect(); return c.display!=='none'&&c.visibility!=='hidden'&&r.width>1&&r.height>1; };
  return {show:sh.classList.contains('show'), nom:(document.getElementById('psName')||{}).textContent, sub:(document.getElementById('psSub')||{}).textContent,
    anneaux:q('.kr-c').map(vu), premOnly:q('.prem-only').map(e=>e.className.split(' ')[0]+':'+vu(e)), eux:q('.kr-eux').map(vu),
    lignes:q('#psList .row').length, liste:(document.getElementById('psList')||{}).textContent.slice(0,120),
    dansDevice:!!sh.closest('#device'), frameDansDevice:!!(document.querySelector('.frame')&&document.querySelector('.frame').closest('#device')),
    deviceDansFrame:!!document.getElementById('device').closest('.frame')}; }"""
def page(b):
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    return pg
def shot(pg, nom):
    dev = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
    pg.screenshot(path=os.path.join(OUT, nom + '.png'), clip={'x': dev[0], 'y': dev[1], 'width': dev[2], 'height': dev[3]})
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = page(b)
    noms = pg.evaluate("()=>{ closeAll(); document.getElementById('souffleBtn').click(); return new Promise(r=>setTimeout(()=>r([...document.querySelectorAll('#auraScreen .au-lb')].map(e=>e.textContent.trim())),2500)); }")
    print('prénoms de la rangée :', noms); pg.close()
    for nom in noms + ['moi', 'Zoé (sans Promi)']:
        pg = page(b); arg = 'Zoé' if nom.startswith('Zoé') else nom
        pg.evaluate("(n)=>{closeAll(); openPerson(n);}", arg); pg.wait_for_timeout(1500)
        r = pg.evaluate(VIS); print('%-16s' % nom, json.dumps(r, ensure_ascii=False)); shot(pg, 'var-dark-' + arg.replace(' ', '_')); pg.close()
    # le Cercle
    pg = page(b); pg.evaluate("()=>{document.getElementById('device').classList.add('premium'); closeAll(); openPerson('Marion');}"); pg.wait_for_timeout(1500)
    r = pg.evaluate(VIS); print('CERCLE (#device.premium) Marion', json.dumps(r, ensure_ascii=False)); shot(pg, 'var-dark-Marion-cercle')
    pg.evaluate("()=>{const f=document.querySelector('.frame'); if(f) f.classList.add('premium'); closeAll(); openPerson('Marion');}"); pg.wait_for_timeout(1500)
    r = pg.evaluate(VIS); print('CERCLE (+ .frame.premium) Marion', json.dumps(r, ensure_ascii=False)); pg.close()
    # l'entrée depuis une fiche
    pg = page(b)
    res = pg.evaluate("""async ()=>{ const ids=promises.filter(p=>!p.draft).map(p=>p.id).slice(0,25);
      for(const id of ids){ closeAll(); openDetail(id); await new Promise(r=>setTimeout(r,700));
        const k=[...document.querySelectorAll('.kring[data-p]')].find(e=>{const r=e.getBoundingClientRect(); return r.width>0&&r.height>0;});
        if(k){ const pp=k.getAttribute('data-p'); k.click(); await new Promise(r=>setTimeout(r,900));
          const sh=document.getElementById('personSheet'); return {id:id, p:pp, ouverte:sh.classList.contains('show'), nom:(document.getElementById('psName')||{}).textContent}; } }
      return 'aucune fiche ne montre un disque de personne cliquable'; }""")
    print('ENTRÉE DEPUIS UNE FICHE :', json.dumps(res, ensure_ascii=False)); pg.close()
    b.close()

# ⚑ UN CONTRAT RÉÉCRIT SE PROUVE CONTRE UN VRAI DÉFAUT (CLAUDE.md §7).
# Chaque contrôle réécrit de redteam_ecrans.py (et le contrôle du bloc centré de
# redteam_air.py, qui mord désormais sur l'Aura) est joué deux fois : TEL QUEL (il doit
# passer) puis avec un DÉFAUT posé exprès (il doit être PRIS). Un contrat réécrit qui ne
# prend rien peut être juste ou éteint — les deux se ressemblent dans un rapport vert.
# Les extraits JS sont ceux des batteries, recopiés à l'identique.
import os, sys, os, io, json
from playwright.sync_api import sync_playwright
ICI = os.path.dirname(os.path.abspath(__file__))
INJECTE = '--injecte' in sys.argv
CSS = io.open(os.path.join(ICI, 'aura.css'), encoding='utf-8').read()
MOT = io.open(os.path.join(ICI, 'moteur.js'), encoding='utf-8').read()
JS = io.open(os.path.join(ICI, 'aura.js'), encoding='utf-8').read()

DEBORDE = """(sel)=>{const d=document.getElementById('device').getBoundingClientRect();
  const root=document.querySelector(sel); if(!root)return -1;
  let n=0;
  root.querySelectorAll('*').forEach(e=>{
    const r=e.getBoundingClientRect();
    if(r.width<2||r.height<2)return;
    if(getComputedStyle(e).position==='fixed')return;
    if(r.right>d.right+2||r.left<d.left-2){
      const g=e.closest('[data-glisse]');
      if(g&&g!==e){const gr=g.getBoundingClientRect(), ov=getComputedStyle(g).overflowX;
        if(gr.left>=d.left-2&&gr.right<=d.right+2&&(ov==='hidden'||ov==='auto'||ov==='scroll'))return;}
      n++;}
  });
  return n;}"""
TOI = """()=>{const n=document.querySelector('#auraScreen .au-moi');
  if(!n)return false;return [...n.querySelectorAll('circle.au-arc')].filter(c=>c.getBoundingClientRect().width>0).length>0;}"""
BOULE = """()=>{const c=document.getElementById('auBoule');
  if(!c||!c.width)return false;const im=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
  let n=0;for(let i=3;i<im.length;i+=160)if(im[i]>200)n++;return n>200;}"""
NB = "()=>[...document.querySelectorAll('#auraScreen .au-nb')].map(e=>e.textContent.trim()).filter(Boolean)"
MOT_ = "()=>{const e=document.querySelector('#auraScreen .au-mot');return e?e.textContent.trim():null;}"
PHRASES = ('Rien de ce qui est ici n’a été dit à la légère.', 'Tout ça, tu l’as dit. Et tu l’as fait.',
           'On ne dirait pas comme ça, mais c’est du solide.', 'Il y en a, des paroles tenues.',
           'Et dire que tout ça, c’est toi.', 'La première parole laissera sa trace ici.')
CHIF = """()=>{const o=[];document.querySelectorAll('#auraScreen *').forEach(e=>{
  const r=e.getBoundingClientRect();if(!r.width||!r.height)return;
  const t=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim();
  if(t&&(t.indexOf('%')>=0||/^[\\d\\s.,]+$/.test(t)))o.push(t);});return o;}"""
SIG = """()=>{const o=[];document.querySelectorAll('#auraScreen *').forEach(e=>{
  const r=e.getBoundingClientRect();if(!r.width||!r.height)return;const s=getComputedStyle(e).textShadow||'';
  if(s.indexOf('240, 122, 46')>=0&&s.indexOf('58, 84, 255')>=0)o.push(e.textContent.trim().slice(0,12));});return o;}"""
ORDRE = """()=>{const d=document.getElementById('device').getBoundingClientRect();
  const R=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();
    return r.height?[Math.round(r.top-d.top),Math.round(r.bottom-d.top)]:null;};
  return {boule:R('#auBoule'), nx:R('#auraScreen .au-nx'), lg:R('#auraScreen .au-lg'),
          mo:R('#auraScreen .au-mo h3'), bt:R('#auPartage')};}"""
LEG = "()=>[...document.querySelectorAll('#auraScreen .au-lg span')].map(s=>[s.textContent.trim(),getComputedStyle(s.querySelector('i')).backgroundColor])"
CENTRE = """()=>{const L=document.querySelector('#auraScreen .au-lg');if(!L||!L.getAttribute('data-centre-entre'))return null;
  const p=L.getAttribute('data-centre-entre').split('|'), sc=L.closest('.screen');
  const A=sc.querySelector(p[0]).getBoundingClientRect(), E=L.getBoundingClientRect(), B=sc.querySelector(p[1]).getBoundingClientRect();
  return [+(E.top-A.bottom).toFixed(2), +(B.top-E.bottom).toFixed(2)];}"""
AIR = """()=>{var res=[];document.querySelectorAll('[data-centre-entre]').forEach(function(el){
  if(!el.getClientRects().length) return; var p=el.getAttribute('data-centre-entre').split('|');
  var sc=el.closest('.screen')||document; var A=sc.querySelector(p[0]), B=sc.querySelector(p[1]); if(!A||!B) return;
  var a=A.getBoundingClientRect(), e=el.getBoundingClientRect(), c=B.getBoundingClientRect();
  res.push([+(e.top-a.bottom).toFixed(2), +(c.top-e.bottom).toFixed(2)]);}); return res;}"""
ARCS = """()=>[...document.querySelectorAll('#auraScreen .au-n circle')].map(c=>({
  w:+c.getAttribute('stroke-width'), cls:c.getAttribute('class'), c:getComputedStyle(c).stroke}))"""
SIGS = """()=>{const r=(e)=>{if(!e)return null;const c=getComputedStyle(e);const f=parseFloat(c.fontSize);
  const m=c.textShadow.match(/(-?[\\d.]+)px\\s+(-?[\\d.]+)px/);
  return m? (Math.abs(+m[1])/f).toFixed(3)+'/'+(Math.abs(+m[2])/f).toFixed(3) : null;};
  return [...document.querySelectorAll('.sig')].map(r).filter(Boolean);}"""
ETATS = ['rgb(43, 232, 140)', 'rgb(143, 160, 255)', 'rgb(240, 122, 46)']

def ordre_ok(g):
    o = [g[k] for k in ('boule', 'nx', 'lg', 'mo', 'bt')]
    return all(o) and all(o[i][0] < o[i+1][0] for i in range(4)) and g['nx'][1] <= g['lg'][0] and g['lg'][1] <= g['mo'][0]

L = []
def rapport(nom, sain, pris):
    L.append((nom, sain, pris))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(os.environ.get('APP_AURA', 'http://127.0.0.1:8752/app.html')); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    if INJECTE:
        pg.add_style_tag(content=CSS); pg.add_script_tag(content=MOT); pg.add_script_tag(content=JS)
    def ouvre():
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(200); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>5)"): break
        pg.wait_for_timeout(400)
    def sonde(js):
        pg.evaluate(js)
    ouvre()
    # 1 · rien ne déborde — et l'exemption n'est donnée QUE sous condition
    s0 = pg.evaluate(DEBORDE, '#auraScreen')
    sonde("()=>{const d=document.createElement('div');d.id='__s';d.style.cssText='position:absolute;left:300px;top:700px;width:150px;height:20px;background:red';document.getElementById('auCadre').appendChild(d);}")
    s1 = pg.evaluate(DEBORDE, '#auraScreen')
    sonde("()=>{const d=document.getElementById('__s');d.style.cssText='flex:none;width:150px;height:20px;background:red;margin-left:400px';document.querySelector('#auraScreen .au-nx').appendChild(d);}")
    s2 = pg.evaluate(DEBORDE, '#auraScreen')
    # ⚠ LES DEUX AXES. `overflow-x:visible` à côté d'un `overflow-y:hidden` se RECALCULE en
    #   `auto` (norme CSS) : la rangée rognait toujours, et l'exemption était juste. Le vrai
    #   défaut est une rangée qui ne rogne plus du tout.
    sonde("()=>{const n=document.querySelector('#auraScreen .au-nx');n.style.setProperty('overflow-x','visible','important');n.style.setProperty('overflow-y','visible','important');}")
    s3 = pg.evaluate(DEBORDE, '#auraScreen')
    sonde("()=>{document.getElementById('__s').remove();const n=document.querySelector('#auraScreen .au-nx');n.style.removeProperty('overflow-x');n.style.removeProperty('overflow-y');}")
    rapport('rien ne déborde (sonde hors de tout)', s0 == 0, s1 > 0)
    rapport('  … exemptée dans une rangée glissante qui rogne', s0 == 0, s2 == 0)
    rapport('  … PRISE si la rangée glissante ne rogne pas', s0 == 0, s3 > 0)
    # 2 · le Noyau « toi » porte ses arcs
    a0 = pg.evaluate(TOI); sonde("()=>{document.querySelectorAll('#auraScreen .au-moi circle.au-arc').forEach(c=>c.style.display='none');}")
    a1 = pg.evaluate(TOI); sonde("()=>{document.querySelectorAll('#auraScreen .au-moi circle.au-arc').forEach(c=>c.style.display='');}")
    rapport('le Noyau « toi » porte ses arcs', a0, not a1)
    # 3 · la sphère est peinte
    b0 = pg.evaluate(BOULE)
    sonde("()=>{window.__pe=OrbiteMoteur.peint;OrbiteMoteur.peint=function(){};const c=document.getElementById('auBoule');c.width=c.width;}")
    pg.wait_for_timeout(200); b1 = pg.evaluate(BOULE)
    sonde("()=>{OrbiteMoteur.peint=window.__pe;}"); pg.wait_for_timeout(300)
    rapport('la sphère est peinte', b0, not b1)
    # 4 · « Partager mon Noyau » mène au partage du Noyau
    def porte():
        r = pg.evaluate("()=>{const b=document.getElementById('auPartage');if(!b)return 'absente';b.click();return 'ok';}")
        pg.wait_for_timeout(900)
        sh = pg.evaluate("()=>({ouvert:document.getElementById('shareScreen').classList.contains('show'),noyau:window.shareMode==='noyau'||document.getElementById('shareScreen').classList.contains('shc-noyau')})")
        pg.evaluate("()=>{document.getElementById('shareScreen').classList.remove('show');window.shareMode=null;document.getElementById('shareScreen').classList.remove('shc-noyau');}")
        return r == 'ok' and sh['ouvert'] and sh['noyau']
    p0 = porte(); ouvre()
    sonde("()=>{const b=document.getElementById('auPartage');b.__oc=b.onclick;b.onclick=function(){};}")
    p1 = porte(); sonde("()=>{const b=document.getElementById('auPartage');b.onclick=b.__oc;}"); ouvre()
    rapport('« Partager mon Noyau » mène au partage du Noyau', p0, not p1)
    # 5 · les Noyaux ne portent que l'image et le prénom
    n0 = pg.evaluate(NB); sonde("()=>{const n=document.querySelector('#auraScreen .au-nb');const s=document.createElement('span');s.id='__t';s.textContent='série 3';n.appendChild(s);}")
    n1 = pg.evaluate(NB); sonde("()=>{document.getElementById('__t').remove();}")
    rapport('les Noyaux ne portent que l\'image et le prénom', not n0, bool(n1))
    # 6 · le mot qualifie l'objet
    m0 = pg.evaluate(MOT_); sonde("()=>{const e=document.querySelector('#auraScreen .au-mot');e.__t=e.textContent;e.textContent='ta parole est solide';}")
    m1 = pg.evaluate(MOT_); sonde("()=>{const e=document.querySelector('#auraScreen .au-mot');e.textContent=e.__t;if(window._aura&&_aura.mot)_aura.mot(null);}")
    rapport('le mot qualifie l\'objet (une des phrases de Tom)', m0 in PHRASES, m1 not in PHRASES)
    # 7 · aucun chiffre ni pourcentage — 8 · aucune signature chiffrée
    c0 = pg.evaluate(CHIF); g0 = pg.evaluate(SIG)
    sonde("()=>{const s=document.createElement('div');s.id='__c';s.textContent='67 %';s.style.cssText='position:absolute;left:30px;top:420px;font-size:20px;text-shadow:-2px 1px 0 #F07A2E, 2px -1px 0 #3A54FF';document.getElementById('auCadre').appendChild(s);}")
    c1 = pg.evaluate(CHIF); g1 = pg.evaluate(SIG); sonde("()=>{document.getElementById('__c').remove();}")
    rapport('aucun chiffre ni pourcentage', not c0, bool(c1))
    rapport('aucune signature chiffrée', not g0, bool(g1))
    # 9 · l'ordre de la page
    o0 = ordre_ok(pg.evaluate(ORDRE)); sonde("()=>{const L=document.querySelector('#auraScreen .au-lg');L.__top=[L.style.getPropertyValue('top'),L.style.getPropertyPriority('top')];L.style.setProperty('top','700px','important');}")
    o1 = ordre_ok(pg.evaluate(ORDRE)); sonde("()=>{const L=document.querySelector('#auraScreen .au-lg');if(L.__top&&L.__top[0])L.style.setProperty('top',L.__top[0],L.__top[1]);else L.style.removeProperty('top');L.__top=null;}")
    rapport('sphère, Noyaux, légende, ce que tu as tenu, bouton', o0, not o1)
    # 10 · la légende nomme trois arcs en trois teintes d'état
    def leg_ok(h): return [x[0] for x in h] == ['tenues', 'en cours', 'à tenir'] and [x[1] for x in h] == ETATS
    l0 = leg_ok(pg.evaluate(LEG)); sonde("()=>{const i=document.querySelector('#auraScreen .au-lg span i');i.__b=i.style.background;i.style.background='#8A5CF0';}")
    l1 = leg_ok(pg.evaluate(LEG)); sonde("()=>{const i=document.querySelector('#auraScreen .au-lg span i');i.style.background=i.__b;}")
    rapport('la légende nomme trois arcs en trois teintes d\'état', l0, not l1)
    # 11 · le Studio ne repeint pas les dalles déjà plantées
    def studio(fuite):
        ouvre(); m0 = pg.evaluate("()=>JSON.stringify((window._auraComp||{}).iles||null)")
        pg.evaluate("()=>{try{Toile.setPalette('ocean');}catch(e){}}")
        if fuite:   # la fuite qu'on veut prendre : une dalle qui suivrait le monde COURANT
            pg.evaluate("()=>{window.__mm=promises.map(p=>[p,p.monde]);promises.forEach(p=>{p.monde=Toile.mondeCourant();});}")
        ouvre(); m1 = pg.evaluate("()=>JSON.stringify((window._auraComp||{}).iles||null)")
        pg.evaluate("()=>{try{Toile.setPalette('signal');}catch(e){} (window.__mm||[]).forEach(x=>{x[0].monde=x[1];}); window.__mm=null;}")
        return m0 == m1 and m0 not in ('null', '[]')
    rapport('le Studio ne repeint pas les dalles déjà plantées', studio(False), not studio(True))
    ouvre()
    # 12 · la légende est centrée — le contrat de redteam_ecrans ET celui de redteam_air
    e0 = pg.evaluate(CENTRE); r0 = pg.evaluate(AIR)
    # ⚠ LA SONDE ET LA MESURE DANS LA MÊME TÂCHE. Posées en deux appels, une image pouvait passer entre
    #   elles : la colonne se recalcule (`place()`, toutes les 30 images, quand une de ses entrées bouge)
    #   et réécrit la cote de la légende — la sonde était AVALÉE, et le contrat paraissait éteint
    #   (vu une fois sur 8e579374, non reproduit en rejouant). Le contrat ne change pas : c'est
    #   l'instrument qui ne laisse plus rien s'intercaler.
    e1, r1 = pg.evaluate("()=>{const L=document.querySelector('#auraScreen .au-lg');L.__top=[L.style.getPropertyValue('top'),L.style.getPropertyPriority('top')];"
                         "L.style.setProperty('top',(parseFloat(getComputedStyle(L).top)+9)+'px','important');"
                         "return [(" + CENTRE + ")(), (" + AIR + ")()];}")
    print('      [12] légende : tel quel %s / %s · sondé %s / %s' % (e0, r0, e1, r1))
    sonde("()=>{const L=document.querySelector('#auraScreen .au-lg');if(L.__top&&L.__top[0])L.style.setProperty('top',L.__top[0],L.__top[1]);else L.style.removeProperty('top');L.__top=null;}")
    rapport('redteam_ecrans · la légende est centrée (≤ 1 px)', bool(e0) and abs(e0[0]-e0[1]) <= 1, bool(e1) and abs(e1[0]-e1[1]) > 1)
    rapport('redteam_air · un bloc annoncé centré a des écarts égaux', bool(r0) and all(abs(x[0]-x[1]) <= 1 for x in r0),
            any(abs(x[0]-x[1]) > 1 for x in r1))
    # 13 · les arcs lisibles — 14 · la piste neutre, les arcs disent l'état
    th = 'rgb(42, 44, 52)' if not pg.evaluate("()=>document.getElementById('device').classList.contains('light')") else 'rgb(222, 215, 198)'
    def arcs_ok(t): return bool(t) and min(x['w'] for x in t) >= 6
    def piste_ok(t): return bool(t) and all(x['c'] == th for x in t if x['cls'] == 'au-piste') and all(x['c'] in ETATS for x in t if x['cls'] == 'au-arc')
    t0 = pg.evaluate(ARCS)
    sonde("()=>{const c=document.querySelector('#auraScreen .au-n circle.au-arc');c.__w=c.getAttribute('stroke-width');c.setAttribute('stroke-width','4');}")
    t1 = pg.evaluate(ARCS); sonde("()=>{const c=document.querySelector('#auraScreen .au-n circle.au-arc');c.setAttribute('stroke-width',c.__w);}")
    sonde("()=>{document.querySelector('#auraScreen .au-n circle.au-piste').style.stroke='#8A5CF0';}")
    t2 = pg.evaluate(ARCS); sonde("()=>{document.querySelector('#auraScreen .au-n circle.au-piste').style.stroke='';}")
    rapport('les arcs des Noyaux sont lisibles (6 px et plus)', arcs_ok(t0), not arcs_ok(t1))
    rapport('la piste est neutre, les arcs disent l\'état', piste_ok(t0), not piste_ok(t2))
    # 15 · la signature est identique partout où elle est portée
    def sig_ok(s): return len(s) >= 2 and len(set(s)) == 1
    s0 = pg.evaluate(SIGS)
    sonde("()=>{const e=document.querySelectorAll('.sig')[1];e.style.setProperty('text-shadow','-9px 4px 0 #F07A2E, 7px -3px 0 #3A54FF','important');}")
    s1 = pg.evaluate(SIGS); sonde("()=>{document.querySelectorAll('.sig')[1].style.removeProperty('text-shadow');}")
    rapport('la signature est identique partout où elle est portée', sig_ok(s0), not sig_ok(s1))
    b.close()

print('\n%-58s %-10s %s' % ('contrat réécrit', 'tel quel', 'défaut posé exprès'))
ko = 0
for nom, sain, pris in L:
    print('%-58s %-10s %s' % (nom, 'passe' if sain else 'ÉCHOUE', 'PRIS' if pris else 'NON PRIS — contrat éteint'))
    if not (sain and pris): ko += 1
_rates = [n for n, s_, p_ in L if not (s_ and p_)]
print('\n%s' % ('✅  les %d contrats mordent' % len(L) if not ko else '❌  %d contrat(s) à reprendre : %s' % (ko, ' · '.join(_rates))))
sys.exit(1 if ko else 0)

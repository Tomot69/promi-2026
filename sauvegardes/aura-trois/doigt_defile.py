# LA PORTE DES DALLES AU VRAI DOIGT (événements tactiles CDP, contexte tactile) — Tom, 11 sept. :
# « la distinction toucher / glissement doit valoir aussi sur la rangée : si la colonne défile, un glissement ne doit
#   jamais ouvrir une fiche par accident ».
# Pour l'Aura (« Ce que tu as tenu », colonne #auCadre) et la fiche de Rachel (« Tenu ensemble », colonne .ps-col) :
#   1 · un GLISSEMENT VERTICAL qui part d'une dalle : la colonne doit DÉFILER (scrollTop change) et AUCUNE fiche ne s'ouvre
#   2 · un glissement court (4 pt, sous le seuil de 6) puis lâcher : c'est un toucher — la fiche s'ouvre
#   3 · un TOUCHER : la fiche de CE Promi s'ouvre (cur.id = data-pid) — celle d'openDetail, la même que la carte d'Index
# Et « un seul chemin de code » : window.openPerson est la fonction de la fiche refaite, et les appels nus la trouvent.
import sys
from playwright.sync_api import sync_playwright
APP = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
FI = "()=>({fiche:document.getElementById('detailPoster').classList.contains('show'), cur:(typeof cur!=='undefined'&&cur)?cur.id:null})"
R = []
def t(nom, ok, d=''): R.append((nom, bool(ok), d)); print('%s  %s  %s' % ('OK  ' if ok else 'RATÉ', nom, d))
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    sc = pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().width/390")
    if 'naif' in sys.argv:
        # SONDE — une porte NAÏVE : ouvre la fiche à chaque doigt levé, même après un défilement. Le contrôle 1 doit la PRENDRE.
        pg.evaluate("""()=>{ let c0=null; document.addEventListener('touchstart', e=>{ c0=e.target.closest&&e.target.closest('#auraScreen .au-c, #psCadre .ps-c'); }, true);
            document.addEventListener('touchend', ()=>{ if(!c0) return; const v=c0.getAttribute('data-pid')||(c0.querySelector('canvas[data-pid]')||{getAttribute:()=>null}).getAttribute('data-pid');
              c0=null; if(v) openDetail(+v); }, true); }""")
        print('SONDE : porte naïve posée')
    def touche(pts, dt=16):
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': pts[0][0], 'y': pts[0][1]}]})
        for x, y in pts[1:]:
            pg.wait_for_timeout(dt); cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y}]})
        pg.wait_for_timeout(dt); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    def aura():
        pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}"); pg.wait_for_timeout(250)
        pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(200)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret)"): break
        pg.wait_for_timeout(800)
    def fiche():
        pg.evaluate("()=>{ closeAll(); openPerson('Rachel'); }"); pg.wait_for_timeout(1600)
    CELL = """([sel,col])=>{ const c=[...document.querySelectorAll(sel)].find(c=>{ const r=c.getBoundingClientRect(); if(r.height<=0) return false;
        const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return h && c.contains(h); }); if(!c) return null;
        const v=c.getAttribute('data-pid')||(c.querySelector('canvas[data-pid]')||{getAttribute:()=>null}).getAttribute('data-pid');
        const r=c.getBoundingClientRect(), k=document.querySelector(col);
        return {pid:+v, t:(c.querySelector('span')||{}).textContent, x:r.left+r.width/2, y:r.top+r.height/2, st:k?k.scrollTop:null, sh:k?k.scrollHeight-k.clientHeight:null}; }"""
    for nom, ouvre, sel, col in (('Aura · Ce que tu as tenu', aura, '#auraScreen .au-c', '#auCadre'),
                                 ('fiche de Rachel · Tenu ensemble', fiche, '#psCadre .ps-c', '#psCadre .ps-col')):
        ouvre(); c = pg.evaluate(CELL, [sel, col])
        if not c: t(nom + ' : une dalle touchable', False, 'aucune'); continue
        # 1 · glissement vertical vers le haut, 160 pt, en 12 pas : la colonne défile, rien ne s'ouvre
        touche([(c['x'], c['y'] - i * 160 * sc / 12) for i in range(13)]); pg.wait_for_timeout(700)
        st = pg.evaluate("(col)=>{const k=document.querySelector(col); return k?k.scrollTop:null;}", col); g = pg.evaluate(FI)
        t(nom + ' : un glissement vertical sur « %s » fait défiler la colonne' % c['t'], st is not None and st > (c['st'] or 0) + 20,
          'scrollTop %s → %s (course possible %s)' % (c['st'], st, c['sh']))
        t(nom + ' : … et n\'ouvre AUCUNE fiche', not g['fiche'], str(g))
        # 2 · un tremblé de 4 pt (sous le seuil de 6) : un toucher
        ouvre(); c = pg.evaluate(CELL, [sel, col])
        touche([(c['x'], c['y']), (c['x'] + 2 * sc, c['y'] + 2 * sc), (c['x'] + 4 * sc, c['y'])]); pg.wait_for_timeout(1000); g = pg.evaluate(FI)
        t(nom + ' : un toucher qui tremble de 4 pt ouvre la fiche de « %s »' % c['t'], g['fiche'] and g['cur'] == c['pid'], str(g))
        # 3 · un toucher net
        ouvre(); c = pg.evaluate(CELL, [sel, col])
        touche([(c['x'], c['y'])]); pg.wait_for_timeout(1000); g = pg.evaluate(FI)
        t(nom + ' : un toucher net ouvre SA fiche (Promi %s)' % c['pid'], g['fiche'] and g['cur'] == c['pid'], str(g))
    # le Noyau de l'Aura, au vrai doigt — la porte d'origine (lot-AURA-ORBITE) ; le clic fantôme la refermait
    PERS = "()=>document.getElementById('personSheet').classList.contains('show') ? (document.getElementById('psCadre')||{getAttribute:()=>'(ancienne)'}).getAttribute('data-fiche') : null"
    aura(); n = pg.evaluate("""()=>{const n=document.querySelector('#auraScreen .au-gp .au-n'); if(!n) return null; const r=n.querySelector('.au-nb').getBoundingClientRect();
        return {qui:n.getAttribute('data-qui'), x:r.left+r.width/2, y:r.top+r.height/2};}""")
    if n:
        touche([(n['x'], n['y'])]); pg.wait_for_timeout(1500); f = pg.evaluate(PERS)
        t('Aura · toucher le Noyau de %s au vrai doigt ouvre SA fiche, et elle RESTE' % n['qui'], f == n['qui'], 'fiche : %s' % f)
    # un nom écrit (chantier 63), au vrai doigt : « Rachel » dans la ligne d'une Nuée
    pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); openEssaim('potager');}"); pg.wait_for_timeout(1600)
    m = pg.evaluate("""()=>{ const h=document.getElementById('dptQui'); if(!h) return null; const w=document.createTreeWalker(h, NodeFilter.SHOW_TEXT); let n;
        while((n=w.nextNode())){ const k=n.textContent.indexOf('Rachel'); if(k<0) continue; const r=document.createRange(); r.setStart(n,k); r.setEnd(n,k+6);
          const b=r.getBoundingClientRect(); return {x:b.left+b.width/2, y:b.top+b.height/2, texte:h.textContent.trim()}; } return null; }""")
    if m:
        touche([(m['x'], m['y'])]); pg.wait_for_timeout(1500); f = pg.evaluate(PERS)
        t('Nuée · toucher « Rachel » dans « %s » au vrai doigt ouvre SA fiche, et elle RESTE' % m['texte'], f == 'Rachel', 'fiche : %s' % f)
    # LES VRAIS TOUCHERS MARCHENT TOUJOURS — le garde du clic fantôme ne doit rien avaler d'autre que la queue d'un geste
    VIS = """(sel)=>{ const e=[...document.querySelectorAll(sel)].find(e=>{ const r=e.getBoundingClientRect(); if(r.width<=0) return false;
        const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return h && (h===e || e.contains(h)); }); if(!e) return null;
        const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }"""
    #   ✕ FERMER d'une fiche, au doigt
    pg.evaluate("()=>{ closeAll(); openDetail(126); }"); pg.wait_for_timeout(1500)
    fx = pg.evaluate(VIS, '#detailPoster .closeb')
    if fx:
        touche([(fx[0], fx[1])]); pg.wait_for_timeout(1200)
        t('toucher ✕ FERMER referme la fiche, au vrai doigt', not pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"), '')
    else: t('✕ FERMER de la fiche touchable', False, 'introuvable')
    #   une carte d'Index, au doigt : elle ouvre son Promi (la porte de la carte, en onclick)
    pg.evaluate("()=>{ closeAll(); if(window.ouvrirIndex) ouvrirIndex(); else document.getElementById('indexSheet').classList.add('show'); }"); pg.wait_for_timeout(1800)
    ci = pg.evaluate("""()=>{ const e=[...document.querySelectorAll('#indexList .s4-carte')].find(e=>{ const r=e.getBoundingClientRect(); if(r.width<=0) return false;
        const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return h && e.contains(h); }); if(!e) return null; const r=e.getBoundingClientRect();
        return {x:r.left+r.width/2, y:r.top+r.height/2, t:(e.querySelector('.s4-ti')||{}).textContent}; }""")
    if ci:
        touche([(ci['x'], ci['y'])]); pg.wait_for_timeout(1400); g = pg.evaluate(FI)
        t('toucher la carte d\'Index « %s » ouvre son Promi, au vrai doigt' % ci['t'], g['fiche'], str(g))
    else: t('une carte d\'Index touchable', False, 'introuvable')
    # un seul chemin de code vers une personne
    u = pg.evaluate("""()=>({win:typeof window.openPerson, nue:(typeof openPerson==='function') && openPerson===window.openPerson,
        refaite:String(window.openPerson).indexOf('psCadre')>=0 || String(window.openPerson).indexOf('poser(')>=0})""")
    t('un seul chemin : l\'appel nu openPerson EST window.openPerson, la fiche refaite', u['nue'] and u['refaite'], str(u))
    b.close()
rates = [r for r in R if not r[1]]
print('\n%s' % ('✅  %d / %d' % (len(R), len(R)) if not rates else '❌  %d RATÉ(S) sur %d' % (len(rates), len(R))))
sys.exit(1 if rates else 0)

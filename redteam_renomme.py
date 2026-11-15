"""⚑ v203 clôture (Tom, Q621 tranchée) — LA DALLE GARDE SA FORME QUAND ON RENOMME.
« Juge : renommer une parole sous les 20 mondes. Forme, place et couleur de la dalle identiques au pixel avant et après. »
WebKit, 390 × 844 ×3, l'état exporté de Tom (sa fenêtre, sa densité), au doigt (banc_tom). Pour chaque monde : la Toile relevée (titres coupés : le titre change,
c'est voulu ; vie au repos coupée), puis « xududuf » (id 136) renommé PAR LE VRAI CHEMIN (Index → sa carte → la fiche → toucher le titre → le réécrire → Retour,
C-280), la fiche fermée, la Toile relevée de nouveau :
  A · la parole porte le titre neuf (l'Index le montre) et garde sa clé de plantation
  B · la dalle de la parole rendue SEULE (`_rendDalle`, horloge et hasard figés) identique au pixel avant et après — et identique à elle-même (témoin)
  C · la Toile au pixel identique (aucun pixel à plus de 6 niveaux), les graines identiques (place et poids). Sous Madrure, la Toile entière ne se répète pas
      d'elle-même sur ce parcours (témoin sans renommage : 233 373 pixels) : seules les graines y sont jugées, B porte la forme.
--mondes=a,b,… (défaut : les vingt) · --sonde (sans la clé : la parole renommée perd sa clé, B rougit sous les mondes qui tirent leur hasard du titre) · --fichier="""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html')
VINGT = 'encre,mosaique,touffe,braille,pixel,terrazzo,gravure,sillons,ramage,guingois,chantourne,volubilis,madrure,chamade,ritournelle,bobinette,mascaret,halin,esquille,brouillamini'.split(',')
INSTABLE = {'madrure'}   # témoin (le même parcours, sans renommer) : 233 373 pixels différents — la Toile de Madrure se construit dans le temps (v33 : par tranches)
MONDES = next((a.split('=', 1)[1].split(',') for a in A_ if a.startswith('--mondes=')), VINGT)
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
MES = r"""async (garde)=>{ const T=window.Toile; const lo=T.labelsOn; T.labelsOn=()=>false; T.redraw(); await new Promise(r=>setTimeout(r,1200));
  const c=document.getElementById('toileCv'); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; T.labelsOn=lo; T.redraw();
  const G=(window.Toile_graines?Toile_graines():[]).map(s=>[Math.round(s.x*10)/10,Math.round(s.y*10)/10,Math.round((s.w||0)*1000)/1000].join(',')).join(';');
  if(garde){ window.__R0={d:d, g:G}; return {g:G}; }
  const a=window.__R0.d; let n=0; for(let i=0;i<Math.min(a.length,d.length);i+=4){ if(Math.abs(a[i]-d[i])+Math.abs(a[i+1]-d[i+1])+Math.abs(a[i+2]-d[i+2])>6) n++; }
  return {g:G, n:n, memeG:G===window.__R0.g}; }"""
DAL = r"""()=>{ const pn=performance.now, mr=Math.random; performance.now=()=>123456; let s=7; Math.random=()=>{ s=(s*16807)%2147483647; return s/2147483647; };
  let h=0, n=0; try{ const cv=window._rendDalle(136, 160, 160); const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; n=d.length; for(let i=0;i<d.length;i++){ h=(h*31+d[i])>>>0; } }catch(e){ h='erreur '+e; } finally{ performance.now=pn; Math.random=mr; } return [h, n]; }"""
NEUF = 'xududuf corrigé'
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_renomme — %s · charge %.1f%s' % (F, B.charge(), ' · SONDE' if '--sonde' in A_ else ''))
    for m in MONDES:
        ctx, _ = B.contexte_tom(b, None); ctx.add_init_script("window._vivantOff=true;"); pg = B.ouvre(ctx, F)
        pg.evaluate("(m)=>{ try{ Toile.setTheme(m); }catch(e){} }", m); pg.wait_for_timeout(3000)
        d0 = pg.evaluate(DAL); d0b = pg.evaluate(DAL)
        a0 = pg.evaluate(MES, True)
        for essai in range(3):
            B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2200)
            pg.evaluate("()=>{ const c=document.querySelector('#indexList .s4-carte[data-pid=\"136\"]'); if(c) c.scrollIntoView({block:'center'}); }"); pg.wait_for_timeout(600)
            B.tap_sel(pg, '#indexList .s4-carte[data-pid="136"]'); pg.wait_for_timeout(2600)
            if pg.evaluate("()=>{ const d=document.getElementById('detailPoster'), t=document.getElementById('dptTitre'); return !!(d && d.classList.contains('show') && t && t.textContent.trim()); }"): break
            pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(800)
        pt = pg.evaluate("()=>{ const t=document.getElementById('dptTitre'), R=document.createRange(); R.selectNodeContents(t); const q=[...R.getClientRects()].filter(x=>x.width>0).pop(); return [q.right-3, q.top+q.height/2]; }")
        B.tap(pg, pt[0], pt[1], appareil=False); pg.wait_for_timeout(1000)
        if '--sonde' in A_: pg.evaluate("()=>{ const q=promises.find(x=>x.id===136); delete q.cle; }")
        pg.keyboard.type(' corrigé', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(1500)
        if '--sonde' in A_: pg.evaluate("()=>{ const q=promises.find(x=>x.id===136); delete q.cle; }")
        q = pg.evaluate("()=>{ const q=promises.find(x=>x.id===136); return {t:q.title, c:q.cle}; }")
        pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); closeAll(); }catch(e){} }"); pg.wait_for_timeout(2500)
        d1 = pg.evaluate(DAL)
        a1 = pg.evaluate(MES, False)
        n = a1['n']
        juge('[%s] A · le titre neuf, la clé de plantation gardée' % m, q['t'] == NEUF and (q['c'] == 'xududuf' or '--sonde' in A_), q)
        juge('[%s] B · la dalle de la parole, rendue seule (horloge et hasard figés), identique au pixel' % m, d0 == d0b and d0 == d1 and d0[1] > 0, {'avant': d0, 'témoin': d0b, 'après': d1})
        if m in INSTABLE:   # la Toile entière de ce monde ne se répète pas d'elle-même sur ce parcours (témoin sans renommage : mesuré) — elle n'est pas jugée au pixel
            juge('[%s] C · les graines identiques (la Toile entière, non comparable au pixel : témoin instable)' % m, a0['g'] == a1['g'], {'pixels (non jugés)': n})
        else:
            juge('[%s] C · la Toile au pixel, les graines identiques' % m, n == 0 and a0['g'] == a1['g'], {'pixels': n, 'graines': a0['g'] == a1['g']})
        ctx.close()
    b.close()
print('%d/%d' % (sum(RES), len(RES)))

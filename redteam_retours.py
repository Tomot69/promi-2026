"""⚑ v203 clôture (Tom, §2) — TOUS LES TEXTES QUI REVIENNENT PASSENT PAR LE MÊME TRACÉ (C-279).
« Liste tous les endroits de l'app où un texte d'exemple, de remplacement ou d'origine réapparaît. Chacun passe par le même code de retour et le même tracé. Juge :
pour chacun, effacement complet puis retour, image par image. Aucun retour sec. »
WebKit, 390 × 844 ×3, au doigt (banc_tom), clavier simulé. Chaque `TraceLettres.trace` est relevé (l'élément, son sens). Les cas (les places à exemple de la page +
et de l'onboarding ont leurs juges : redteam_exemple_retour, redteam_onb_exemple ; le titre vidé d'une fiche : redteam_titre_fiche E) :
  ix · la recherche de l'Index (« Rechercher ») · fd · la recherche du Fil · np · la description d'un Cercle, dans Peaufiner (« présente le Cercle, son but… »)
  mot · « Un mot… » d'une fiche · gn · l'ajout d'une personne (« + ajouter quelqu’un », « un prénom… ») · li · « de » / « d’ » de la page +
Pour chacun :
  P · à la première lettre, le texte d'exemple se DÉTRACE (une copie à sa place, à rebours) et la lettre est là tout de suite
  R · effacé (ou refermé), il revient par un TRACÉ
  S · pas sec, image par image (relevé dans la page) : dès la première image après l'effacement une transition est en cours (déclarée, `__dcA`) et, pour un champ simple,
      le texte natif est caché (il ne paraît qu'à la fin du tracé, exactement sous la copie : A)
  F · à la fin : le texte entier (un champ simple : l'image du texte natif, au pixel hors du bord des lettres), et plus rien de la transition (ni copie, ni texte natif caché)
  A · (les champs simples) la copie qui se trace est posée EXACTEMENT sur le texte natif qu'elle remplace : aucun pixel changé hors du bord des lettres
  E · (les champs simples) au focus, le texte d'exemple devient « … » (le curseur, lot-CURSEUR) : l'ancien se détrace PUIS « … » se trace ; au départ du focus,
      l'inverse — jamais d'un coup
--cas=ix,fd,np,mot,gn,li · --sonde (le retour d'un coup, comme avant : R et S rougissent) · --fichier="""
import sys, io, json; sys.path.insert(0, '.')
import banc_tom as B
from collections import Counter
from PIL import Image, ImageChops, ImageFilter
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html')
CAS = next((a.split('=', 1)[1].split(',') for a in A_ if a.startswith('--cas=')), ['ix', 'fd', 'np', 'mot', 'gn', 'li'])
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
INIT = r"""(()=>{ window.__R=[]; (function arme(){ const T=window.TraceLettres; if(!T || !T.trace){ setTimeout(arme, 50); return; } if(T.__r) return; T.__r=1; const o=T.trace;
  T.trace=function(el, c, op){ op=op||{}; if(!op.preparer && el) window.__R.push({t:performance.now(), inv:!!op.inverse, cl:(typeof el.className==='string'?el.className:'')+'#'+(el.id||''), txt:(el.textContent||'').trim().slice(0,30)}); return o.apply(this, arguments); }; })(); })();"""
SONDE = r"""(()=>{ (function a(){ if(!window._retour){ setTimeout(a, 50); return; } const R=window._retour; R.champ=function(){ return {}; }; R.bascule=function(el, m){ el.style.display=m?'':'none'; }; R.remplace=function(el, f){ f(); }; R.motLigne=function(l, m, s, o){ m.style.display=(o && s && s.value)?'none':''; }; })(); })();"""
def zone(pg, sel):
    return pg.evaluate("(s)=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return {x:r.left-2, y:r.top-2, width:r.width+4, height:r.height+4}; }", sel)
def encre(pg, z):
    if not z: return 0
    im = Image.open(io.BytesIO(pg.screenshot(clip=z))).convert('RGB'); px = list(im.getdata()); W, H = im.size
    bord = [im.getpixel((x, 0)) for x in range(W)] + [im.getpixel((x, H - 1)) for x in range(W)]; fond = Counter(bord).most_common(1)[0][0]
    return sum(1 for q in px if sum(abs(q[j] - fond[j]) for j in range(3)) > 90)
def hors_lettres(a, b):
    fond = Counter(a.getdata()).most_common(1)[0][0]
    enc = Image.new('L', a.size); enc.putdata([255 if sum(abs(q[j] - fond[j]) for j in range(3)) > 24 else 0 for q in a.getdata()]); pres = enc.filter(ImageFilter.MaxFilter(5))
    d = ImageChops.difference(a, b).convert('L'); return sum(1 for v, m in zip(d.getdata(), pres.getdata()) if v > 24 and not m)
REC = r"""()=>{ window.__F=[]; window.__K=null; document.addEventListener('input', function k(){ window.__K=performance.now(); document.removeEventListener('input', k, true); }, true);
  const t0=performance.now(); (function f(){ const a=document.activeElement, en=window.__dcA ? [...window.__dcA].some(e=>e && e.isConnected) : false;
    window.__F.push([performance.now(), en, !!(a && a.classList && a.classList.contains('v203-phx'))]); if(performance.now()-t0<700) requestAnimationFrame(f); })(); }"""
def images(pg): pg.wait_for_timeout(800); return pg.evaluate("()=>(window.__F||[]).filter(x=>window.__K!=null && x[0]>=window.__K).map(x=>[x[0]-window.__K, x[1], x[2]])")
def sec(F, natif):
    """les deux premières images après la touche : un tracé en cours (et le natif caché)"""
    d = F[:2]
    return bool(d) and all(x[1] and (x[2] or not natif) for x in d)
def traces(pg, t0, inv): return [x for x in pg.evaluate("()=>window.__R") if x['t'] >= t0 and x['inv'] == inv]
def propre(pg): return pg.evaluate("()=>!document.querySelector('.v203-ph, .v203-rempl, .v203-ex') && !document.querySelector('.v203-phx')")
def champ_simple(pg, nom, sel, txt):
    """un champ simple : son texte d'exemple natif"""
    tf = pg.evaluate("()=>performance.now()")
    for _ in range(3):
        B.tap_sel(pg, sel); pg.wait_for_timeout(700)
        if pg.evaluate("(s)=>document.activeElement===document.querySelector(s)", sel): break
    pg.wait_for_timeout(1600)
    e1a = [x['txt'] for x in traces(pg, tf, True) if 'v203-ph' in x['cl']]; e1b = [x['txt'] for x in traces(pg, tf, False) if 'v203-ph' in x['cl']]
    # A · la copie exactement sur le texte natif
    z = zone(pg, sel); a = Image.open(io.BytesIO(pg.screenshot(clip=z))).convert('RGB')
    pg.evaluate("(s)=>{ const i=document.querySelector(s); i.classList.add('v203-phx'); window.__g=(window._retour && window._retour.fantome) ? window._retour.fantome(i, i.getAttribute('placeholder')) : null; }", sel); pg.wait_for_timeout(120)   # une version sans le composant : aucune copie (A rougit)
    b = Image.open(io.BytesIO(pg.screenshot(clip=z))).convert('RGB'); pg.evaluate("(s)=>{ document.querySelector(s).classList.remove('v203-phx'); if(window.__g) window.__g.remove(); }", sel)
    n_al = hors_lettres(a, b); e_fin = encre(pg, z)
    t0 = pg.evaluate("()=>performance.now()"); pg.keyboard.press('a'); pg.wait_for_timeout(40)
    v1 = pg.evaluate("(s)=>document.querySelector(s).value", sel); pg.keyboard.type('bc', delay=60); pg.wait_for_timeout(700)
    p = [x for x in traces(pg, t0, True) if 'v203-ph' in x['cl']]
    t1 = pg.evaluate("()=>performance.now()")
    for _ in range(2): pg.keyboard.press('Backspace'); pg.wait_for_timeout(50)
    pg.evaluate(REC); pg.keyboard.press('Backspace'); FF = images(pg); pg.wait_for_timeout(1800)
    r = [x for x in traces(pg, t1, False) if 'v203-ph' in x['cl']]
    z = zone(pg, sel); e1 = encre(pg, z); pr = propre(pg)
    juge('[%s] P · première lettre : la lettre tout de suite, l\'exemple se détrace' % nom, v1 == 'a' and p, {'valeur': v1, 'détracés': len(p)})
    juge('[%s] R · effacé, « %s » revient par son tracé' % (nom, txt), r, len(r))
    juge('[%s] S · pas sec : dès la première image, le tracé est en cours et le texte natif caché' % nom, sec(FF, True), [x[1:] for x in FF[:3]])
    c1 = Image.open(io.BytesIO(pg.screenshot(clip=z))).convert('RGB'); nf = hors_lettres(a, c1) if c1.size == a.size else -1   # le texte d'exemple du champ focalisé, avant la frappe et après l'effacement : le même
    if nf: a.save('scratchpad/v203g/F-%s-avant.png' % nom[:2]); c1.save('scratchpad/v203g/F-%s-fin.png' % nom[:2])
    juge('[%s] F · à la fin, le texte natif entier (hors du bord des lettres : %d pixel(s)), plus rien de la transition' % (nom, nf), pr and nf == 0, {'propre': pr})
    juge('[%s] A · la copie est posée exactement sur le texte natif (hors du bord des lettres : %d pixel(s))' % (nom, n_al), n_al == 0)
    juge('[%s] E · au focus, « %s » se détrace puis « … » se trace (le curseur)' % (nom, txt), txt in e1a and '…' in e1b, {'détracés': e1a, 'tracés': e1b})
    tb = pg.evaluate("()=>performance.now()"); pg.evaluate("()=>{ document.activeElement.blur(); }"); pg.wait_for_timeout(1800)
    e2a = [x['txt'] for x in traces(pg, tb, True) if 'v203-ph' in x['cl']]; e2b = [x['txt'] for x in traces(pg, tb, False) if 'v203-ph' in x['cl']]
    juge('[%s] E · au départ du focus, « … » se détrace puis « %s » se trace' % (nom, txt), '…' in e2a and txt in e2b and propre(pg), {'détracés': e2a, 'tracés': e2b})
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_retours — %s · charge %.1f%s' % (F, B.charge(), ' · SONDE' if '--sonde' in A_ else ''))
    def ctx_(etat=10):
        c = B.contexte(b); B.toile_pleine(c, etat); c.add_init_script(CLAV); c.add_init_script(INIT)
        if '--sonde' in A_: c.add_init_script(SONDE)
        return c
    if 'ix' in CAS or 'fd' in CAS:
        c = ctx_(); pg = B.ouvre(c, F)
        if 'ix' in CAS:
            B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2200); champ_simple(pg, 'ix · recherche de l\'Index', '#ixSearch', 'Rechercher'); pg.evaluate("()=>{ document.activeElement.blur(); closeAll(); }"); pg.wait_for_timeout(900)
        if 'fd' in CAS:
            B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2200); champ_simple(pg, 'fd · recherche du Fil', '#fdSearch', 'Rechercher')
        c.close()
    if 'np' in CAS:
        c = ctx_('cercle'); pg = B.ouvre(c, F)
        B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2200); pg.evaluate("()=>{ const c=document.querySelector('#indexList .s4-carte[data-nk]'); if(c) c.scrollIntoView({block:'center'}); }"); pg.wait_for_timeout(400)
        B.tap_sel(pg, '#indexList .s4-carte[data-nk]'); pg.wait_for_timeout(2600); B.tap_sel(pg, '#dpDetails'); pg.wait_for_timeout(1800)
        champ_simple(pg, 'np · description d\'un Cercle', '#nqNote', 'présente le Cercle, son but…'); c.close()
    if 'mot' in CAS or 'li' in CAS or 'gn' in CAS:
        c = ctx_(); pg = B.ouvre(c, F)
        if 'mot' in CAS:
            B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2200); B.tap_sel(pg, '#indexList .s4-carte[data-pid]'); pg.wait_for_timeout(2600)
            sel = '#detailPoster .cm5-ligne, #detailPoster [class*=cm5-l]'
            lig = pg.evaluate("()=>{ const m=document.querySelector('#detailPoster .cm5-mot'); if(!m) return null; const l=m.parentNode; l.id=l.id||'__ligneMot'; return '#'+l.id; }")
            m_sel = '#detailPoster .cm5-mot'
            for _ in range(3):
                B.tap_sel(pg, m_sel); pg.wait_for_timeout(800)
                if pg.evaluate("()=>{ const a=document.activeElement; return !!(a && a.classList && a.classList.contains('cm5-saisie')); }"): break
            z = zone(pg, m_sel); e_fin = encre(pg, z) if z else 0
            t0 = pg.evaluate("()=>performance.now()"); pg.keyboard.press('a'); pg.wait_for_timeout(40)
            v1 = pg.evaluate("()=>document.activeElement.value"); pg.keyboard.type('bc', delay=60); pg.wait_for_timeout(800)
            pp = [x for x in traces(pg, t0, True) if 'cm5-mot' in x['cl']]
            t1 = pg.evaluate("()=>performance.now()")
            for _ in range(2): pg.keyboard.press('Backspace'); pg.wait_for_timeout(50)
            pg.evaluate(REC); pg.keyboard.press('Backspace'); FF = images(pg); pg.wait_for_timeout(1800); z = zone(pg, m_sel); e1 = encre(pg, z)
            rr = [x for x in traces(pg, t1, False) if 'cm5-mot' in x['cl']]
            juge('[mot · « Un mot… »] P · première lettre : la lettre tout de suite, « Un mot… » se détrace', v1 == 'a' and pp, {'valeur': v1, 'détracés': len(pp)})
            juge('[mot · « Un mot… »] R · effacé, « Un mot… » revient par son tracé', rr, len(rr))
            juge('[mot · « Un mot… »] S · pas sec : dès la première image, le tracé est en cours', sec(FF, False), [x[1:] for x in FF[:3]])
            juge('[mot · « Un mot… »] F · entier à la fin (ouvert, vide), plus rien de la transition', propre(pg) and e1 > 0.8 * e_fin, {'encre': e1, 'fermé': e_fin})
            t2 = pg.evaluate("()=>performance.now()"); pg.keyboard.type('x', delay=40); pg.wait_for_timeout(700)
            pg.evaluate("()=>{ document.activeElement.blur(); }"); pg.evaluate("()=>{ try{ _peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(1500)
        if 'li' in CAS:
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
            for _ in range(3):
                B.tap_sel(pg, '#csPhrase [data-ph=titre]'); pg.wait_for_timeout(900)
                if pg.evaluate("()=>{const a=document.activeElement;return !!a&&a.id==='phIn';}"): break
            t0 = pg.evaluate("()=>performance.now()"); pg.keyboard.type('aller', delay=60); pg.wait_for_timeout(1800)
            li1 = pg.evaluate("()=>{ const l=document.querySelector('#csPhrase [data-ph=titre]').previousElementSibling; return l?l.textContent:null; }")
            d1 = [x for x in traces(pg, t0, True) if 'ph-li' in x['cl']]; r1 = [x for x in traces(pg, t0, False) if 'ph-li' in x['cl']]
            t1 = pg.evaluate("()=>performance.now()")
            for _ in range(5): pg.keyboard.press('Backspace'); pg.wait_for_timeout(60)
            pg.wait_for_timeout(2500)
            li2 = pg.evaluate("()=>{ const l=document.querySelector('#csPhrase [data-ph=titre]').previousElementSibling; return l?l.textContent:null; }")
            d2 = [x for x in traces(pg, t1, True) if 'ph-li' in x['cl']]; r2 = [x for x in traces(pg, t1, False) if 'ph-li' in x['cl']]
            juge('[li · « de » → « d’ »] P · détracé puis tracé', li1 == 'd’' and d1 and r1, {'mot': li1, 'détracés': len(d1), 'tracés': len(r1)})
            juge('[li · « d’ » → « de »] R · détracé puis tracé', li2 == 'de' and d2 and r2, {'mot': li2, 'détracés': len(d2), 'tracés': len(r2)})
            pg.evaluate("()=>{ document.activeElement.blur(); }")
        if 'gn' in CAS:
            pg.wait_for_timeout(600)
            if not pg.evaluate("()=>!!document.querySelector('#createSheet.show')"):
                B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
            pg.evaluate("()=>{ const s=document.querySelector('#csPhrase [data-ph=sens]'); if(s) s.click(); }"); pg.wait_for_timeout(1500)
            B.tap_sel(pg, '#csPhrase [data-ph=qui]'); pg.wait_for_timeout(1500)
            zsel = '.gn .ph-add'
            ok0 = pg.evaluate("(s)=>{ const z=document.querySelector(s); return z?z.textContent.trim():null; }", zsel)
            t0 = pg.evaluate("()=>performance.now()"); B.tap_sel(pg, zsel); pg.wait_for_timeout(1500)
            a1 = traces(pg, t0, True); f1 = traces(pg, t0, False)
            ph_v = pg.evaluate("()=>{ const p=document.querySelector('.gn .gn-ph'); return p?getComputedStyle(p).display:null; }")
            t1 = pg.evaluate("()=>performance.now()"); pg.keyboard.type('Zo', delay=80); pg.wait_for_timeout(900)
            dp = [x for x in traces(pg, t1, True) if 'gn-ph' in x['cl']]
            t2 = pg.evaluate("()=>performance.now()")
            for _ in range(2): pg.keyboard.press('Backspace'); pg.wait_for_timeout(60)
            pg.wait_for_timeout(2000); rp = [x for x in traces(pg, t2, False) if 'gn-ph' in x['cl']]
            juge('[gn · ajouter quelqu’un] P · à l\'ouverture, « %s » se détrace et la saisie se trace' % ok0, ok0 and any('v203-rempl' in x['cl'] for x in a1) and f1, {'détracés': len(a1), 'tracés': len(f1)})
            juge('[gn · « un prénom… »] P · première lettre : « un prénom… » se détrace', dp, len(dp))
            juge('[gn · « un prénom… »] R · effacé, il revient par son tracé', rp and pg.evaluate("()=>{ const p=document.querySelector('.gn .gn-ph'); return !!p && getComputedStyle(p).display!=='none'; }"), len(rp))
            t3 = pg.evaluate("()=>performance.now()"); pg.evaluate("()=>{ document.activeElement.blur(); }"); pg.wait_for_timeout(1800)
            fr = traces(pg, t3, False); z2 = pg.evaluate("(s)=>{ const z=document.querySelector(s); return z?z.textContent.trim():null; }", zsel)
            juge('[gn · refermé] R · « + ajouter quelqu’un » revient par son tracé', z2 == '+ ajouter quelqu’un' and any('ph-add' in x['cl'] for x in fr) and propre(pg), {'texte': z2, 'tracés': [x['cl'][:20] for x in fr][:4]})
        c.close()
    b.close()
print('%d/%d' % (sum(RES), len(RES)))

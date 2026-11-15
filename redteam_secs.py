"""⚑ v201b (Tom, C-271) — AUCUN CHANGEMENT SEC : les points de AUDIT-SECS.md rejoués image par image.

Un relevé dans la page, à chaque image (WebKit, ×3, 430 × 932) :
  T · un texte visible qui change à sa place sans transition déclarée (ni tracé, ni détracé, ni fondu, ni découpe) est une faute ;
  B · une rangée ou une carte (repérée par sa clé : data-v, data-pid, data-nk) qui saute de plus de 12 pt d'une image à l'autre sans animation en cours est une faute.
La frappe elle-même n'est pas jugée (ce qu'on tape s'écrit lettre par lettre). Le parcours : la page + des trois natures (bascule, validation, choix, Rachel ajoutée,
retirée), l'Index (recherche, tri), le Fil, l'Aura, les Réglages (une valeur basculée), le Studio (quatre mondes), une fiche (un mot envoyé : le nombre, « Les Mots »).
--fichier= ; --sonde : les transitions de v201b coupées (window._flip = rendu direct, aucun observateur) — il rougit.
"""
import sys, os; sys.path.insert(0, '.'); A = sys.argv[1:]; sys.argv = [sys.argv[0]]
src = open('redteam_moi_phrase.py', encoding='utf-8').read(); src = src[:src.index('with sync_playwright() as p:\n    b = p.webkit')]; ns = {'__file__': 'redteam_moi_phrase.py'}; exec(compile(src, 'm', 'exec'), ns)
B = ns['B']; pose = ns['pose']; stable = ns['stable']
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in A if a.startswith('--fichier=')), 'app.html'); SONDE = '--sonde' in A
REC = """(()=>{ if(window.__au) return; window.__au=[]; window.__auEtape=''; window.__auPause=false; const D=()=>document.getElementById('device'); let prev=new Map(), prevB=new Map();
  function nom(e){ let s=''; const reg=e.closest&&e.closest('.s2-reg'), lab=reg&&reg.querySelector('.s2-lab'); if(lab) s='{'+lab.textContent.trim()+'}'; if(e.classList&&e.classList.contains('v201-n')) e=e.parentElement; for(let x=e,i=0;x&&x.nodeType===1&&i<4;x=x.parentElement,i++){ const ph=x.getAttribute&&(x.getAttribute('data-ph')||x.getAttribute('data-np')); s=(x.id?'#'+x.id:(x.className&&typeof x.className==='string'?'.'+x.className.trim().split(/\\s+/)[0]:x.tagName.toLowerCase()))+(ph?'['+ph+']':'')+(s?' > '+s:''); if(x.id) break; } return s; }
  function trans(e){ for(let x=e;x&&x.nodeType===1;x=x.parentElement){ if(x.__trace||x.__v200) return true; const c=x.style&&(x.style.clipPath||x.style.webkitClipPath); if(c&&c!=='none') return true; if(x.getAnimations && x.getAnimations().some(a=>{ try{ const c=a.effect&&a.effect.getComputedTiming(); return a.playState==='running' && c && isFinite(c.activeDuration); }catch(_){ return false; } })) return true; } return false; }
  function saisie(e){ return !!(e.closest && e.closest('.gn-txt, input, textarea, [contenteditable]')) || (document.activeElement && document.activeElement.tagName==='INPUT' && e.closest && e.closest('[data-ph="titre"],[data-np="nom"]')); }
  function tour(){ const dv=D(); if(dv && !window.__auPause){ const R=dv.getBoundingClientRect(), s=R.width/390, cur=new Map(); const w=document.createTreeWalker(document.querySelector('.frame')||document.body, NodeFilter.SHOW_TEXT); let t, k=0;
      while((t=w.nextNode()) && k<3000){ const v=t.nodeValue.trim(); if(!v) continue; const e=t.parentElement; if(!e || e.closest('.v201-part, .v201-val')) continue; const r=e.getBoundingClientRect(); if(!r.width||r.bottom<R.top||r.top>R.bottom||r.right<R.left||r.left>R.right) continue;
        const cs=getComputedStyle(e); if(cs.visibility==='hidden'||+cs.opacity<0.05) continue; k++;
        const cleB=e.closest('[data-v],[data-pid],[data-nk]'), un=e.closest('.cm5-un'); const nm=(cleB?('['+(cleB.getAttribute('data-v')||cleB.getAttribute('data-pid')||cleB.getAttribute('data-nk'))+'] '):'')+(un?'['+(un.querySelector('.cm5-t')||un).textContent.slice(0,24)+'] ':'')+nom(e);
        let j=0; while(cur.has(nm+'@'+j) && cur.get(nm+'@'+j).e!==e) j++; const key=nm+'@'+j; const o=cur.get(key); cur.set(key, {e:e, v:(o?o.v:'')+v, tr:trans(e)||saisie(e)}); }
      cur.forEach((c,key)=>{ const o=prev.get(key); if(o && o.v!==c.v && !c.tr && !o.tr) window.__au.push({etape:window.__auEtape, quoi:'T', el:key, de:o.v.slice(0,40), vers:c.v.slice(0,40)}); });
      prev=cur; const curB=new Map();
      (document.querySelector('.frame')||document.body).querySelectorAll('.gn-liste > .ph-o[data-v], #indexList .s4-carte[data-pid], #indexList .s4-carte[data-nk], #feedList .s4-carte[data-pid], #cm5Liste .cm5-un').forEach(b=>{ let r=b.getBoundingClientRect(); if(!r.width) return; let an=b.parentElement; while(an && an!==document.body){ const st=getComputedStyle(an); if(/(auto|scroll)/.test(st.overflowY) && an.scrollHeight>an.clientHeight+1) break; an=an.parentElement; }
        if(an && an!==document.body){ const ar=an.getBoundingClientRect(), es=(an.offsetWidth?ar.width/an.offsetWidth:1)||1; r={left:r.left-ar.left+an.scrollLeft*es+R.left, top:r.top-ar.top+an.scrollTop*es+R.top, width:r.width, an:an}; }   /* le repère de ce qui défile : un défilement n'est pas un saut */
        const k2=(b.getAttribute('data-v')||b.getAttribute('data-pid')||b.getAttribute('data-nk')||((b.querySelector('.cm5-t')||b).textContent.slice(0,24)))+'|'+(b.closest('#indexList')?'ix':b.closest('#feedList')?'fd':b.closest('#cm5Liste')?'mots':'gn'); curB.set(k2,{x:r.left/s, y:r.top/s, a:trans(b), an:r.an||null}); });
      curB.forEach((c,k2)=>{ const o=prevB.get(k2); if(o && o.an===c.an && !c.a && !o.a && Math.hypot(c.x-o.x, c.y-o.y)>12) window.__au.push({etape:window.__auEtape, quoi:'B', el:k2, de:o.y.toFixed(0), vers:c.y.toFixed(0)}); });
      prevB=curB; }
    requestAnimationFrame(apres); }
  /* ⚠ v123 : un relevé pris DANS un rappel d'image passe avant les autres rappels de la même image — il lit un état qui ne sera jamais peint. On lit APRÈS l'image. */
  const MC=new MessageChannel(); MC.port1.onmessage=tour; function apres(){ MC.port2.postMessage(0); }
  requestAnimationFrame(apres); })()"""
SND = "()=>{ window._flip=function(b,s,c,r){ return r(); }; window.MutationObserver=function(){ return {observe(){}, disconnect(){}, takeRecords(){ return []; }}; }; }"
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-70s %s' % ('✅' if ok else '❌', nom, str(d)[:400]), flush=True)
def etape(pg, n): pg.evaluate("n=>{ window.__auEtape=n; }", n)
def scroll_tout(pg): pg.evaluate("()=>{ window.__auPause=true; }"); pg.wait_for_timeout(80); pg.evaluate("()=>{ window.__auPause=false; }")
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 10); ctx.add_init_script(REC)
    if SONDE: ctx.add_init_script(SND)
    pg = B.ouvre(ctx, F); pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} }"); pg.wait_for_timeout(800)
    print('redteam_secs — %s, charge %.1f%s' % (F, B.charge(), ' · SONDE' if SONDE else ''), flush=True)
    ETAPES = []
    for K in ('promi', 'chiche', 'nuee'):
        e = 'page + ' + K; ETAPES.append(e); etape(pg, e)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % K); pg.wait_for_timeout(2600)
        if K == 'promi': B.tap_sel(pg, '#csPhrase .ph-b[data-ph="sens"]'); pg.wait_for_timeout(1500)
        pose(pg, K, 'lire un livre'); stable(pg, K); pg.wait_for_timeout(3500)
        sel = '#nueePhrase .ph-m[data-np="avec"]' if K == 'nuee' else '#csPhrase .ph-m[data-ph="qui"]'
        B.tap_sel(pg, sel); pg.wait_for_timeout(1500)
        B.tap_sel(pg, '#createSheet .gn > .ph-add'); pg.wait_for_timeout(400); pg.keyboard.type('Rachel', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
        pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(2000)
        try: B.tap_sel(pg, '#createSheet .gn .gn-liste .ph-o.on[data-v="Rachel"] .ppo-x'); pg.wait_for_timeout(2000)
        except Exception: pass
        B.tap(pg, 195, 200); pg.wait_for_timeout(2500); pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(1500)
    for nom, js in (('Index', "document.getElementById('indexBtn').click()"), ('Fil', "document.getElementById('filBtn').click()"), ('Aura', "document.getElementById('souffleBtn').click()"), ('Réglages', "document.getElementById('settingsBtn').click()")):
        ETAPES.append(nom); etape(pg, nom); pg.evaluate("()=>{ closeAll(); " + js + "; }"); pg.wait_for_timeout(3000)
        if nom == 'Index':
            pg.evaluate("()=>{ const s=document.querySelector('#indexSearch, #ixRecherche, #indexScreen input[type=search], #indexSheet input'); if(s){ s.focus(); s.value='li'; s.dispatchEvent(new Event('input',{bubbles:true})); } }"); pg.wait_for_timeout(1500)
            pg.evaluate("()=>{ const s=document.activeElement; if(s && s.tagName==='INPUT'){ s.value=''; s.dispatchEvent(new Event('input',{bubbles:true})); s.blur(); } }"); pg.wait_for_timeout(1500)
        if nom == 'Aura':   # une parole tenue, l'Aura ouverte : ses deux chiffres changent
            pg.evaluate("()=>{ const p=promises.find(x=>x.status==='encours'&&!x.draft); p.status='tenu'; try{ syncAll(); }catch(e){} try{ window._paroles && _paroles.publie(); }catch(e){} }"); pg.wait_for_timeout(2500)
        if nom == 'Réglages':
            pg.evaluate("()=>{ const r=document.getElementById('setMention'); if(r) r.click(); }"); pg.wait_for_timeout(1200)
    ETAPES.append('Studio'); etape(pg, 'Studio'); pg.evaluate("()=>{ closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
    for i in range(4): B.glisse(pg, B.droite([300, 420], [90, 420], 10), pas=16); pg.wait_for_timeout(2200)
    ETAPES.append('Peaufiner'); etape(pg, 'Peaufiner'); pg.evaluate("()=>{ closeAll(); const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.chiche); openDetail(p.id); }"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{ const t=document.getElementById('dpdTog'); if(t) t.click(); }"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ const r=[...document.querySelectorAll('#dpdCorps .s2-reg')].find(r=>/AVANT/.test((r.querySelector('.s2-lab')||{}).textContent||'')); if(r && !r.classList.contains('s2-ouv')) r.click(); }"); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{ const b=[...document.querySelectorAll('#dpdCorps .s2-reg button, #dpdCorps .s2-reg .chip')].find(b=>/1 sem/.test(b.textContent)); if(b) b.click(); }"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ try{ window._peaufSortie && _peaufSortie(); }catch(e){} }"); pg.wait_for_timeout(600)
    ETAPES.append('fiche'); etape(pg, 'fiche'); pg.evaluate("()=>{ closeAll(); const p=promises.find(x=>x.status==='encours'&&!x.draft&&!x.chiche); p.comments=[]; openDetail(p.id); }"); pg.wait_for_timeout(3000)
    r = pg.evaluate("""async ()=>{ const l=document.getElementById('cm5Ligne'); if(!l) return 'pas de ligne'; const q=l.getBoundingClientRect(), m=l.querySelector('.cm5-mot')||l;
        const pe=(el,typ,x,y)=>el.dispatchEvent(new PointerEvent(typ,{bubbles:true,cancelable:true,pointerId:9,pointerType:'touch',isPrimary:true,clientX:x,clientY:y}));
        for(const t of ['Premier mot','Second mot']){ pe(m,'pointerdown',q.left+60,q.top+20); pe(m,'pointerup',q.left+60,q.top+20); await new Promise(z=>setTimeout(z,450));
          const s=l.querySelector('.cm5-saisie'); if(!s) return 'pas de saisie'; s.value=t; s.dispatchEvent(new Event('input',{bubbles:true}));
          const f=l.querySelector('.cm5-va'), r=f.getBoundingClientRect(); pe(f,'pointerdown',r.left+r.width/2,r.top+r.height/2); pe(f,'pointerup',r.left+r.width/2,r.top+r.height/2); await new Promise(z=>setTimeout(z,1600)); }
        return 'ok'; }""")
    pg.wait_for_timeout(1500)
    A2 = pg.evaluate("()=>window.__au")
    for e in ETAPES:
        L = [x for x in A2 if x['etape'] == e]
        vus = {}
        for x in L: vus.setdefault((x['quoi'], x['el']), x)
        juge('[%s] aucun texte ni aucune boîte ne change d’un coup' % e, not L, ['%s %s « %s » → « %s »' % (x['quoi'], x['el'][:60], x['de'], x['vers']) for x in list(vus.values())[:6]])
    err = [x for x in pg.erreurs if 'version.json' not in x]; juge('aucune erreur de page', not err, err[:2])
    b.close()
ok = sum(res); print('\n  %s %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res))); sys.exit(0 if ok == len(res) else 1)

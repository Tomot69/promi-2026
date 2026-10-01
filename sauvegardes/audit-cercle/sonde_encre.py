# SONDE : pour la PREMIÈRE ligne de chaque champ, (1) les fragments qui la composent, (2) sa police, (3) l'ENCRE des premières
# lettres (canvas.measureText, même police) : où commence vraiment le dessin, par rapport à la boîte de ligne.
from playwright.sync_api import sync_playwright
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
J = r"""(sels)=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390; const cv=document.createElement('canvas').getContext('2d'); const out={};
  for(const [nom, sel] of sels){ const c=document.querySelector(sel); if(!c){ out[nom]=null; continue; } const r=c.getBoundingClientRect(); const fr=[];
    const w=document.createTreeWalker(c,NodeFilter.SHOW_TEXT); let n;
    while((n=w.nextNode())){ if(!n.textContent.trim()) continue; const p=n.parentElement; if(!p.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})||p.closest('textarea')) continue;
      const g=document.createRange(); g.selectNodeContents(n); const q=[...g.getClientRects()].filter(q=>q.width>1)[0]; if(!q) continue; const k=getComputedStyle(p);
      const font=k.fontStyle+' '+k.fontWeight+' '+k.fontSize+' '+k.fontFamily; cv.font=font; const txt=n.textContent.trim(); const m1=cv.measureText(txt.slice(0,2)), mf=cv.measureText('Hg');
      // la boîte de contenu d'un texte en ligne va de (ligne de base − ascendante de police) à (+ descendante) : l'encre commence à ascendante − hauteur d'encre des lettres
      const asc=mf.fontBoundingBoxAscent, desc=mf.fontBoundingBoxDescent, base=q.top + (q.height-(asc+desc))/2 + asc;
      fr.push({txt:txt.slice(0,18), font:k.fontWeight+' '+k.fontSize+'/'+k.lineHeight+' '+k.fontFamily.split(',')[0], boite_t:+((q.top-r.top)/s).toFixed(2), boite_b:+((q.bottom-r.top)/s).toFixed(2), l:+((q.left-r.left)/s).toFixed(2),
        encre_t:+((base-m1.actualBoundingBoxAscent-r.top)/s).toFixed(2), encre_l:+((q.left-m1.actualBoundingBoxLeft-r.left)/s).toFixed(2), encre_b:+((base+m1.actualBoundingBoxDescent-r.top)/s).toFixed(2)}); }
    out[nom]={h:+(r.height/s).toFixed(1), frag:fr.sort((a,b)=>a.boite_t-b.boite_t)}; }
  return out; }"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width':430,'height':932}, device_scale_factor=2).new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("()=>setTheme('dark')")
    pg.evaluate(BASE); pg.evaluate("()=>openDetail(126)"); pg.wait_for_timeout(1400); pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1700)
    pg.evaluate("""()=>{ const L=[...document.querySelectorAll('#detailPoster .s2-liste > .s2-reg')]; const f=(t)=>L.find(r=>((r.querySelector('.s2-lab')||r).textContent||'').trim()===t);
      f('À QUI').id=f('À QUI').id||'sqQui'; f('PIÈCES JOINTES').id='sqPJ'; f('NOTE').id='sqNote'; }""")
    R = pg.evaluate(J, [['À QUI (64)', '#sqQui'], ['PJ fiche (92)', '#sqPJ'], ['NOTE fiche (118)', '#sqNote']])
    pg.evaluate(BASE); pg.evaluate("()=>openEssaim('potager')"); pg.wait_for_timeout(1500); pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1700)
    R.update(pg.evaluate(J, [['Nuée MEMBRES (64)', '#npMemb'], ['Nuée PJ (92)', '#npFich'], ['Nuée DESCRIPTION (104)', '#npDesc'], ['Nuée LE TRAIT (118)', '#npTrait']]))
    for k, v in R.items():
        print('\n==', k, 'h', v and v['h'])
        for f in (v['frag'] if v else [])[:4]: print('   ', f)
    br.close()

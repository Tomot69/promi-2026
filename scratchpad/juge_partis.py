from playwright.sync_api import sync_playwright
JS = r"""()=>{
  const OK={'Bricolage':[600,700],'Apfel':[400],'ApfelMid':[500],'Fraunces':[600]};
  const bad={petit:[],opac:[],degrade:[],ombre:[],police:[],tonsurton:[]};
  const lum=c=>{const m=c.match(/\d+/g); if(!m) return null;
    if(m.length>3 && +m[3]===0) return null;
    return 0.299*+m[0]+0.587*+m[1]+0.114*+m[2];};
  document.querySelectorAll('.fr').forEach((f,fi)=>{
    const fondL=lum(getComputedStyle(f).backgroundColor);
    f.querySelectorAll('*').forEach(n=>{
      const cs=getComputedStyle(n), r=n.getBoundingClientRect();
      if(cs.display==='none'||cs.visibility==='hidden'||r.width<1) return;
      const t=[...n.childNodes].some(c=>c.nodeType===3&&c.nodeValue.trim());
      const L=fi+' «'+(n.textContent||'').replace(/\s+/g,' ').trim().slice(0,24)+'»';
      if(t){
        if(parseFloat(cs.fontSize)<12) bad.petit.push(L+' → '+cs.fontSize);
        if(+cs.opacity<0.72&&+cs.opacity>0) bad.opac.push(L+' → '+cs.opacity);
        const fam=(cs.fontFamily||'').split(',')[0].replace(/["']/g,''), fw=parseInt(cs.fontWeight);
        if(OK[fam]){ if(OK[fam].indexOf(fw)<0) bad.police.push(L+' → '+fam+' '+fw); }
        else bad.police.push(L+' → HORS '+fam+' '+fw);
        // ton sur ton : l'encre du texte contre CE QUI EST PEINT dessous
        let sous=null, p=n;
        while(p&&p!==f.parentNode){ const b=lum(getComputedStyle(p).backgroundColor);
          if(b!==null){sous=b;break;} p=p.parentElement; }
        if(sous===null) sous=fondL;
        const enc=lum(cs.color);
        if(enc!==null&&sous!==null&&Math.abs(enc-sous)<42)
          bad.tonsurton.push(L+' → Δlum '+Math.round(Math.abs(enc-sous)));
      }
      if(/gradient/.test(cs.backgroundImage)) bad.degrade.push(L);
      if(cs.boxShadow!=='none') bad.ombre.push(L+' box');
      if(cs.textShadow!=='none') bad.ombre.push(L+' text');
    });
  });
  return bad;
}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1800,'height':1200}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/PLANCHE-AURA-TROIS-PARTIS.html')
    pg.wait_for_function("()=>window.__pret===true", timeout=30000); pg.wait_for_timeout(2000)
    r=pg.evaluate(JS)
    tot=0
    for k,v in r.items():
        tot+=len(v)
        print(f'── {k.upper()} : {len(v)}')
        for x in v[:12]: print('   ',x)
    print(('✅  LA LANGUE EST TENUE' if tot==0 else f'❌  {tot} écarts'))
    b.close()

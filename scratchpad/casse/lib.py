# -*- coding: utf-8 -*-
"""Boîte à outils de la passe d'usage. On SE SERT de l'app, on ne la mesure pas."""
R = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
URL = "http://127.0.0.1:8752/app.html"

# ── superpositions + débordements, sur l'écran tel qu'il est ────────────────────────────
CHEVAUCHE = r"""(racine)=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const hote = racine? document.querySelector(racine) : document.body;
  if(!hote) return {sup:[], deb:[], n:0};
  const vis=e=>{const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.35) return false;
    const r=e.getBoundingClientRect(); return r.width>6&&r.height>6;};
  const nom=e=>(e.id?'#'+e.id:'.'+(e.className+'').split(' ').filter(Boolean).slice(0,2).join('.')).slice(0,34);
  const txt=e=>((e.textContent||'').trim().replace(/\s+/g,' ')).slice(0,30);
  // on ne compare que ce qui PORTE quelque chose : du texte sans enfant élément, ou une image
  const feuilles=[...hote.querySelectorAll('*')].filter(e=>{
    if(!vis(e)) return false;
    if(e.tagName==='CANVAS'||e.tagName==='IMG'||e.tagName==='SVG') return false;
    const t=(e.textContent||'').trim();
    if(!t) return false;
    return [...e.children].every(c=>['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(c.tagName)
                                     && !(c.textContent||'').trim().includes('\n'));
  });
  const box=e=>{const r=e.getBoundingClientRect();
    return {x:(r.left-dev.left)/sc,y:(r.top-dev.top)/sc,w:r.width/sc,h:r.height/sc,r:r};};
  const sup=[];
  for(let i=0;i<feuilles.length;i++) for(let j=i+1;j<feuilles.length;j++){
    const a=feuilles[i],b=feuilles[j];
    if(a.contains(b)||b.contains(a)) continue;
    const A=box(a),B=box(b);
    const ix=Math.max(0,Math.min(A.x+A.w,B.x+B.w)-Math.max(A.x,B.x));
    const iy=Math.max(0,Math.min(A.y+A.h,B.y+B.h)-Math.max(A.y,B.y));
    if(ix<3||iy<3) continue;
    const inter=ix*iy, petit=Math.min(A.w*A.h,B.w*B.h);
    if(inter/petit < 0.22) continue;
    sup.push(nom(a)+' « '+txt(a)+' » ⨯ '+nom(b)+' « '+txt(b)+' »  ('+Math.round(100*inter/petit)+'% sur '
      +Math.round(Math.min(A.y,B.y))+')');
  }
  const deb=[];
  [...hote.querySelectorAll('*')].filter(vis).forEach(e=>{
    const B=box(e);
    if(B.w>420||B.h>1200) return;
    if(B.x<-1.5||B.x+B.w>391.5) deb.push(nom(e)+' « '+txt(e)+' » de x='+Math.round(B.x)+' à '+Math.round(B.x+B.w));
    else if(B.y+B.h>846 && getComputedStyle(e).position!=='static'
            && !e.closest('#indexList,#feedList,.dpd-corps,.s2-liste'))
      deb.push(nom(e)+' « '+txt(e)+' » descend à y='+Math.round(B.y+B.h));
  });
  return {sup:[...new Set(sup)].slice(0,25), deb:[...new Set(deb)].slice(0,20), n:feuilles.length};
}"""

# ── les contours pointillés : lesquels, et sont-ils vides ? ─────────────────────────────
POINTILLE = r"""(racine)=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const hote = racine? document.querySelector(racine) : document.body;
  if(!hote) return [];
  const out=[];
  [...hote.querySelectorAll('*')].forEach(e=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden') return;
    if(!/dashed|dotted/.test(c.borderTopStyle+c.outlineStyle)) return;
    const r=e.getBoundingClientRect(); if(r.width<8||r.height<8) return;
    out.push((e.id?'#'+e.id:'.'+(e.className+'').split(' ').filter(Boolean).slice(0,2).join('.'))
      +' @'+Math.round((r.left-dev.left)/sc)+','+Math.round((r.top-dev.top)/sc)
      +' '+Math.round(r.width/sc)+'x'+Math.round(r.height/sc)
      +' style='+(/dashed|dotted/.test(c.borderTopStyle)?c.borderTopStyle:c.outlineStyle)
      +' « '+((e.textContent||'').trim().replace(/\s+/g,' ').slice(0,40))+' »');
  });
  return [...new Set(out)].slice(0,20);
}"""

PREP = """()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"""

# -*- coding: utf-8 -*-
"""TOUS LES DISQUES VISIBLES DU PRODUIT : le filet creme est-il COLLE au bord exterieur ?
   On mesure sur le canevas/SVG lui-meme, rayon par rayon, seulement ce qui est A L'ECRAN."""
import json,sys
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
SONDE = r"""()=>{
  function mesureCanvas(cv){
    var W=cv.width,H=cv.height,cx=W/2,cy=H/2,g=cv.getContext('2d');
    var d; try{ d=g.getImageData(0,0,W,H).data; }catch(e){ return null; }
    function px(x,y){var o=(y*W+x)*4;return [d[o],d[o+1],d[o+2],d[o+3]];}
    var ring=null, cf=null, cl=null;
    for(var r=0;r<cx;r+=0.25){
      var x=Math.round(cx+r), y=Math.round(cy); if(x>=W)break;
      var c=px(x,y);
      var creme=Math.abs(c[0]-247)<18&&Math.abs(c[1]-240)<18&&Math.abs(c[2]-222)<20&&c[3]>120;
      if(c[3]>30 && !creme) ring=r;
      if(creme){ if(cf===null)cf=r; cl=r; }
    }
    var b=cv.getBoundingClientRect();
    return {type:'canvas', W:W, cssW:+b.width.toFixed(1), ring:ring, cremeDe:cf, cremeA:cl,
            jeuPx:(cf!==null&&ring!==null)?+((cf-ring)*(b.width/W)).toFixed(2):null,
            decl:cv.getAttribute('data-filet')};
  }
  function mesureSvg(n){
    var s=n.querySelector('svg'); if(!s) return null;
    var vb=(s.getAttribute('viewBox')||'').split(/\s+/).map(Number); var D=vb.length===4?vb[2]:0;
    var f=s.querySelector('circle.kr-filet'); if(!f) return {type:'svg', D:D, filet:null};
    var a=s.querySelector('path.au-arc,circle.au-arc');
    var ro=null;
    if(a){ var r=+(a.getAttribute('r')||0), ep=+(a.getAttribute('stroke-width')||0);
      if(!r){ var m=(a.getAttribute('d')||'').match(/A(\d+(?:\.\d+)?)/); if(m) r=+m[1]; }
      ro=r+ep/2; }
    var rf=+f.getAttribute('r'), fw=+f.getAttribute('stroke-width');
    return {type:'svg', D:D, ringOut:ro, filetInt:+(rf-fw/2).toFixed(2), jeuPx:(ro!==null)?+((rf-fw/2)-ro).toFixed(2):null};
  }
  var out=[];
  document.querySelectorAll('canvas.kr-c').forEach(function(cv){
    var b=cv.getBoundingClientRect(); if(b.width<8) return;
    var p=cv.closest('.screen,.poster,.sheet,#personSheet,#detailPoster'); 
    var m=mesureCanvas(cv); if(m){ m.ou=(p?p.id||p.className:'?'); out.push(m); }
  });
  document.querySelectorAll('.au-nb').forEach(function(n){
    var b=n.getBoundingClientRect(); if(b.width<8) return;
    var m=mesureSvg(n); if(m){ m.ou='auNoyau'; out.push(m); }
  });
  return out;
}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    res={}
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
        for nom,js,wt in (
            ('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}",5200),
            ('personne',"()=>{closeAll(); openPerson('Marion');}",3200),
            ('fiche-tenue',"()=>{closeAll(); var q=promises.find(function(p){return p.status==='tenu'&&!p.nuee;}); if(q) openDetail(q.id);}",3600),
            ('cercle',"()=>{closeAll(); if(window.ouvreCercle) ouvreCercle();}",3200)):
            pg.evaluate(js); pg.wait_for_timeout(wt)
            res[nom+'/'+th]=pg.evaluate(SONDE)
            pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(700)
    b.close()
for k,v in res.items():
    print('══',k)
    for m in v:
        print('   ',json.dumps(m,ensure_ascii=False))

# -*- coding: utf-8 -*-
import json
from playwright.sync_api import sync_playwright
OUT={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

    # --- 6 · palettes
    OUT['palettes']=pg.evaluate("()=>{var P=window.Toile.palettes(); return {n:Object.keys(P).length, ordre:Object.keys(P)};}")

    # --- 3 · largeur de « LE CERCLE » en PromiLate, police chargée
    OUT['titre_px']=pg.evaluate(r"""async ()=>{ await document.fonts.ready;
      var c=document.createElement('canvas').getContext('2d'); var o={};
      [26,28,29,30,32,34].forEach(function(s){ c.font='400 '+s+'px PromiLate'; o[s]=+c.measureText('LE CERCLE').width.toFixed(2); });
      return o; }""")

    # --- 2+3 : ouvrir par « Promi »
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(500)
    pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(1400)
    pg.click('.acc-plat .acc-mm'); pg.wait_for_timeout(2600)
    OUT['porte']=pg.evaluate(r"""()=>{ var ps=document.getElementById('plusScreen');
      var h=document.querySelector('#plusScreen #pcCadre .pc-h');
      var cs=h?getComputedStyle(h):null; var r=h?h.getBoundingClientRect():null;
      return {cercleOuvert:!!(ps&&ps.classList.contains('show')),
              texte:h?h.textContent:null, police:cs?cs.fontFamily:null, taille:cs?cs.fontSize:null,
              larg:r?+r.width.toFixed(1):null, lignes:h?Math.round(h.getBoundingClientRect().height):null}; }""")
    open('scratchpad/s26/V12-cercle-dark.png','wb').write(pg.query_selector('#device').screenshot())
    pg.evaluate("(t)=>setTheme(t)",'light'); pg.wait_for_timeout(700)
    open('scratchpad/s26/V12-cercle-light.png','wb').write(pg.query_selector('#device').screenshot())

    # --- 1 · le filet des Noyaux (Aura, sombre)
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(500)
    pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5400)
    OUT['filet_aura']=pg.evaluate(r"""()=>{ var out=[];
      document.querySelectorAll('#auraScreen canvas.kr-c').forEach(function(cv,i){ if(i>2)return;
        var g=cv.getContext('2d'),W=cv.width,cx=W/2,cy=cv.height/2;
        var d=g.getImageData(0,0,W,cv.height).data;
        function px(x,y){var o=(y*W+x)*4;return [d[o],d[o+1],d[o+2],d[o+3]];}
        var last=null, cf=null, cl=null, ringLast=null;
        for(var r=0;r<cx;r+=0.5){ var x=Math.round(cx+r), y=Math.round(cy); if(x>=W)break;
          var c=px(x,y);
          var creme=Math.abs(c[0]-247)<16&&Math.abs(c[1]-240)<16&&Math.abs(c[2]-222)<18&&c[3]>120;
          if(c[3]>20){ last=r; if(!creme) ringLast=r; }
          if(creme){ if(cf===null)cf=r; cl=r; } }
        out.push({i:i, W:W, decl:cv.getAttribute('data-filet'), ringLast:ringLast, cremeDe:cf, cremeA:cl, jeu:(cf!==null&&ringLast!==null)?+(cf-ringLast).toFixed(1):null});
      }); return out; }""")
    open('scratchpad/s26/V12-aura-dark.png','wb').write(pg.query_selector('#device').screenshot())

    # --- 1b · le filet du + de l'accueil
    pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(1500)
    OUT['filet_plus']=pg.evaluate(r"""()=>{var b=document.getElementById('createBtn'); if(!b)return null;
      var cs=getComputedStyle(b), r=b.getBoundingClientRect();
      var be=getComputedStyle(b,'::before');
      return {w:+r.width.toFixed(1), outline:cs.outlineWidth+' '+cs.outlineStyle+' '+cs.outlineColor, offset:cs.outlineOffset, beforeInset:be.inset||be.top};}""")

    # --- 4 · le Fil
    pg.evaluate("()=>{document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3400)
    OUT['fil']=pg.evaluate(r"""()=>{ var o={n:document.querySelectorAll('#feedList .s4-carte').length,
        comp:(window._filComp||[]).length, cartes:[]};
      document.querySelectorAll('#feedList .s4-carte').forEach(function(d){
        var t=d.querySelector('.s4-ti'), v=d.querySelector('.s4-ev'), e=d.querySelector('.s4-et'), cv=d.querySelector('canvas');
        var rt=t.getBoundingClientRect(), rv=v?v.getBoundingClientRect():null, re=e?e.getBoundingClientRect():null;
        o.cartes.push({titre:t.textContent, cote:d.getAttribute('data-titre-cote'),
          fs:getComputedStyle(t).fontSize, scroll:t.scrollHeight, client:t.clientHeight,
          top:t.style.top, evTop:v?v.style.top:null, champ:cv?cv.getAttribute('data-champ'):null,
          peint:cv?cv.getAttribute('data-peint'):null});
      }); return o; }""")
    open('scratchpad/s26/V12-fil-dark.png','wb').write(pg.query_selector('#device').screenshot())

    # --- 5 · le retour du Studio
    pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(900)
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
        pg.evaluate("()=>{closeAll(); document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2600)
        pg.evaluate("()=>{var s=document.getElementById('studioScreen'); s.classList.add('stp-pals'); if(window._studioRetour)window._studioRetour();}")
        pg.wait_for_timeout(1500)
        OUT['retour_'+th]=pg.evaluate(r"""()=>{var b=document.querySelector('.stp-retour'), pl=document.getElementById('stpPals');
          var cs=b?getComputedStyle(b):null, cp=pl?getComputedStyle(pl):null;
          return {color:cs?cs.color:null, fill:cs?cs.webkitTextFillColor:null, bord:cs?cs.borderTopColor:null,
                  panneau:cp?cp.backgroundColor:null, nPals:document.querySelectorAll('#stpPals .st3-p').length};}""")
        open('scratchpad/s26/V12-studiopals-%s.png'%th,'wb').write(pg.query_selector('#device').screenshot())
        pg.evaluate("()=>{closeAll(); var s=document.getElementById('studioScreen'); s.classList.remove('stp-pals');}"); pg.wait_for_timeout(500)
    OUT['erreurs']=errs
    b.close()
print(json.dumps(OUT,indent=1,ensure_ascii=False))

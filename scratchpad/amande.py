# -*- coding: utf-8 -*-
"""L'AMANDE #8FE08F NE DOIT PEINDRE QUE L'ANIMATION DE CÉLÉBRATION.
   On parcourt les écrans et on relève TOUT ce qui est peint en #8FE08F — fond, texte, trait."""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
AM='rgb(143, 224, 143)'
JS=r"""(am)=>{var out=[];
 document.querySelectorAll('*').forEach(function(e){
  var cs=getComputedStyle(e), r=e.getBoundingClientRect();
  if(r.width<1||r.height<1||cs.display==='none'||cs.visibility==='hidden') return;
  var q=[];
  if(cs.backgroundColor===am) q.push('fond');
  if(cs.color===am && (e.textContent||'').trim() && e.children.length===0) q.push('texte');
  if(cs.borderTopColor===am||cs.borderLeftColor===am) q.push('bordure');
  var st=e.getAttribute && e.getAttribute('stroke'); if(st && st.toUpperCase()==='#8FE08F') q.push('trait');
  if(!q.length) return;
  var cls=(typeof e.className==='string')?e.className.trim().split(/\s+/).slice(0,2).join('.'):'';
  out.push(q.join('+')+' · '+(e.id?'#'+e.id:'')+(cls?'.'+cls:e.tagName)+' · «'+(e.textContent||'').trim().slice(0,22)+'»');});
 return out;}"""
ECR=[('accueil',''),('aura',"document.getElementById('souffleBtn').click()"),
 ('index',"document.getElementById('indexBtn').click()"),('fil',"document.getElementById('filBtn').click()"),
 ('page+',"document.getElementById('createBtn').click()"),
 ('fiche tenue',"for(var i=1;i<=220;i++){try{var p=promises.filter(function(q){return q.id===i})[0];if(p&&!p.draft&&p.status==='tenu'){openDetail(i);break}}catch(e){}}"),
 ('nuée',"try{window.openNueeDetail(Object.keys(NUE)[0])}catch(e){}"),
 ('partage',"var b=document.getElementById('shareBtn');b&&b.click()")]
tot=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    for theme in ('sombre','clair'):
        for nom,js in ECR:
            pg.goto(URL); pg.wait_for_timeout(6000)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", 'light' if theme=='clair' else 'dark'); pg.wait_for_timeout(400)
            if js:
                try: pg.evaluate("()=>{%s}"%js)
                except Exception: pass
                pg.wait_for_timeout(2200)
            for r in pg.evaluate(JS, AM):
                k='%s · %s · %s'%(theme,nom,r)
                if k not in tot: tot.append(k); print('  ',k)
    b.close()
print()
print('%d surface(s) peinte(s) en amande hors animation.'%len(tot))

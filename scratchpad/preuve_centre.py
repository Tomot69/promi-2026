# ⚑ UN CONTROLE NEUF SE PROUVE CONTRE UN VRAI DEFAUT — sinon il peut etre
#   juste OU ETEINT, et les deux se ressemblent dans un rapport vert.
#   L'ecran Aura n'est pas encore dans app.html : le controle y trouve zero
#   noeud declare et se tait. On le prouve donc sur la planche, ou il vit.
from playwright.sync_api import sync_playwright
SONDE = """(dy)=>{
  var res=[];
  document.querySelectorAll('[data-centre-entre]').forEach(function(el){
    if(dy) el.style.top=(parseFloat(getComputedStyle(el).top)+dy)+'px';
    var p=el.getAttribute('data-centre-entre').split('|');
    var sc=el.closest('.ec2')||el.closest('.screen')||document;
    var A=sc.querySelector(p[0]), B=sc.querySelector(p[1]);
    if(!A||!B) return;
    var a=A.getBoundingClientRect(), e=el.getBoundingClientRect(), c=B.getBoundingClientRect();
    res.push([+(e.top-a.bottom).toFixed(2), +(c.top-e.bottom).toFixed(2)]);
  });
  return res;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1300,'height':1000})
    pg.goto('http://127.0.0.1:8752/PLANCHE-VELOURS.html')
    pg.wait_for_function("()=>window.__pret===true",timeout=300000); pg.wait_for_timeout(500)
    for titre,dy in (("tel quel", 0), ("avec un defaut de 9 px pose exprès", 9)):
        r=pg.evaluate(SONDE, dy)
        pris=[x for x in r if abs(x[0]-x[1])>1.0]
        print("%-38s %d bloc(s) declare(s)   PRIS : %d" % (titre, len(r), len(pris)))
        for x in r: print("      au-dessus %6.2f   en dessous %6.2f   ecart %5.2f" % (x[0],x[1],abs(x[0]-x[1])))
    b.close()

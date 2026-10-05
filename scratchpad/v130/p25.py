import io
S=io.open('redteam_decoupe.py',encoding='utf-8').read()
old="""  Toile.dalleTrame=function(dcv,pid,k,monde,opts){ const r=f.apply(this,arguments);
    if(monde&&monde.m&&monde.m!==Toile.getTheme()) return r;   /* une dalle rendue EXPRÈS dans un autre monde (les exemples) n'est pas de cette mesure */"""
new="""  Toile.dalleTrame=function(dcv,pid,k,monde,opts){ const r=f.apply(this,arguments);
    if(monde&&monde.m&&monde.m!==Toile.getTheme()) return r;   /* une dalle rendue EXPRÈS dans un autre monde (les exemples) n'est pas de cette mesure */
    /* ⚠ et le monde RÉELLEMENT peint se lit sur ce que le moteur déclare (`__dalleInfo.monde`), jamais sur le thème supposé : l'app
       rend aussi des dalles dans le monde de son Studio (icônes de la page +, décor de l'Aura), qui n'est pas forcément celui que le
       juge vient de poser — vu : un cœur de Chamade compté comme « une autre couleur » sous Tesselle (1 passage sur 2). */
    try{ const mi=dcv.__dalleInfo&&dcv.__dalleInfo.monde; if(mi&&mi.m&&window.__g2m&&mi.m!==window.__g2m) return r; }catch(e){}"""
assert S.count(old)==1; S=S.replace(old,new)
old="""                pg.evaluate("(m)=>{closeAll(); Toile.setTheme(m); window.__g2.length=0;}", m); pg.wait_for_timeout(2500)"""
new="""                pg.evaluate("(m)=>{closeAll(); Toile.setTheme(m); window.__g2m=m; window.__g2.length=0;}", m); pg.wait_for_timeout(2500)"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('redteam_decoupe.py','w',encoding='utf-8').write(S)

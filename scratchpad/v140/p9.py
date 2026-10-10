import io
S=io.open('app.html',encoding='utf-8').read()
def rep(o,n,c=1):
    global S
    assert S.count(o)==c,(S.count(o),o[:80]); S=S.replace(o,n)
# la page + d'E2 : des sélecteurs qui gagnent
rep("""#device.e2-plus #createSheet #csBotBar, #device.e2-plus #createSheet #csPinceau, #device.e2-plus #createSheet .ph-hint,
#device.e2-plus #createSheet .ph-photo-nid, #device.e2-plus #createSheet .ph-b svg{display:none!important}""",
"""#device#device#device#device.e2-plus #createSheet#createSheet #csBotBar, #device#device#device#device.e2-plus #createSheet#createSheet #csPinceau, #device#device#device#device.e2-plus #createSheet#createSheet .ph-hint,
#device#device#device#device.e2-plus #createSheet#createSheet .ph-photo-nid, #device#device#device#device.e2-plus #createSheet#createSheet .ph-photo-btn, #device#device#device#device.e2-plus #createSheet#createSheet .ph-b svg{display:none!important;visibility:hidden!important}
/* A2 : aucun nœud du chantier n'hérite d'une transition ni d'une animation */
#onbV .e2-principe, #onbV .e2-principe *, #onbV .e2-bouton, #onbV .onbv-tard, #device .e2-tard, #device .e2-ligne, #device #accBarreFond, #device .dv-invite, #dvTout, #dvTout *{transition:none!important;animation:none!important}""")
# le Fil : seulement une parole adressée ou reçue (le journal du Fil porte aussi mes propres gestes)
rep("""    try{ if(typeof FEED!=='undefined' && Array.isArray(FEED) && FEED.some(function(f){ return f && f.who && (''+f.who).toLowerCase()!=='moi'; })) dvPose('fil'); }catch(_){ }
""","")
# la main ne montre le trait de plantation que lorsqu'il y a quelque chose à planter
rep("""      var e=null; try{ e=window._ppEcran && window._ppEcran(); }catch(_){ } var cv=$('csTrameCv'); if(!e || !cv || !e.base) return null;""",
"""      var e=null; try{ e=window._ppEcran && window._ppEcran(); }catch(_){ } var cv=$('csTrameCv'); if(!e || !cv || !e.base) return null;
      /* E2 (v140) : sans titre, tracer ne plante rien (Promi, Chiche) — la main attend que la phrase porte ses mots ; sinon elle se montrait
         sur la pastille vide, partait au toucher qui la remplit, et ne revenait plus pour le trait */
      try{ if(cs.getAttribute('data-kind')!=='nuee' && !(''+((window._phrase||{}).titre||'')).trim()) return null; }catch(_){ }""")
io.open('app.html','w',encoding='utf-8').write(S)
# le juge : un nœud dont un ancêtre est à opacité 0 n'est pas à l'écran ; fermer l'Aura par son ✕, au doigt
J=io.open('redteam_e2.py',encoding='utf-8').read()
o="""const haut=(e)=>{"""
assert J.count(o)==1
J=J.replace("""const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, vis=(e)=>{ if(!e) return false; const r=e.getBoundingClientRect(), c=getComputedStyle(e); return r.width>6&&r.height>6&&c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>0.05; };""",
"""const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, vis=(e)=>{ if(!e) return false; const r=e.getBoundingClientRect(), c=getComputedStyle(e); if(!(r.width>6&&r.height>6&&c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>0.05)) return false;
    if(r.bottom<D.top||r.top>D.bottom||r.right<D.left||r.left>D.right) return false; for(let q=e.parentElement; q&&q.nodeType===1; q=q.parentElement){ const s=getComputedStyle(q); if(+s.opacity<0.05||s.visibility==='hidden'||s.display==='none') return false; if(q.id==='device') break; } return true; };""")
o="""        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(2600)
        e = pg.evaluate(ETAT); note(e); cap(pg, '10-accueil-studio-' + th)"""
assert J.count(o)==1
J=J.replace(o,"""        x = point(pg, '#auraScreen .closeb')
        if x: toucher(cdp, pg, x[0], x[1])
        else: pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }")
        pg.wait_for_timeout(2800)
        e = pg.evaluate(ETAT); note(e); cap(pg, '10-accueil-studio-' + th)""")
io.open('redteam_e2.py','w',encoding='utf-8').write(J)

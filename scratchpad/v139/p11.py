import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
rep("COMBLE_K:0.15,","COMBLE_K:0.08,")
# Q426 : les deux rangées
rep("  if(!rejeu()){ var n=0, t=setInterval(function(){ if(rejeu() || ++n>40) clearInterval(t); }, 250); }",
"""  /* ⚑ v139 (Tom, 9 oct. 2026, Q426) — « Garde les deux rangées, “Revoir la présentation” et “Revoir les gestes”. » La rangée de la présentation
     revient, juste au-dessus de celle des gestes, avec son rôle d'origine (elle relance la présentation) ; elle lit le geste, comme sa voisine. */
  function presentation(){ var c=$('replayOnb'); if(!c) return false; if($('replayPres')) return true;
    var p=document.createElement('div'); p.className='scard'; p.id='replayPres'; p.setAttribute('role','button'); p.tabIndex=0; p.setAttribute('aria-label','Revoir la présentation');
    p.innerHTML='<span class="k">Revoir la présentation</span><span class="v ac">rejouer ›</span>'; c.parentNode.insertBefore(p, c);
    var G=null, tF=0;
    function fait(e){ if(e){ try{ e.preventDefault(); e.stopImmediatePropagation(); }catch(_){ } } if(performance.now()-tF<700) return; tF=performance.now();
      try{ window._tutoSeen=false; $('settingsScreen').classList.remove('show'); replayIntro(); }catch(_){ } }
    p.addEventListener('pointerdown', function(e){ G={x:e.clientX, y:e.clientY, t:performance.now()}; }, true);
    p.addEventListener('pointerup', function(e){ var g=G; G=null; if(!g || Math.hypot(e.clientX-g.x, e.clientY-g.y)>10 || performance.now()-g.t>600) return; fait(e); }, true);
    p.addEventListener('click', fait, true);
    p.addEventListener('keydown', function(e){ if(e.key==='Enter' || e.key===' ') fait(e); });
    return true; }
  if(!(rejeu() && presentation())){ var n=0, t=setInterval(function(){ if((rejeu() && presentation()) || ++n>40) clearInterval(t); }, 250); }""")
rep("#device #gesteFantome svg{position:absolute;left:0;top:0;display:block;max-width:none;overflow:visible}",
"""#device #gesteFantome svg{position:absolute;left:0;top:0;display:block;max-width:none;overflow:visible}
/* v139 (Q426) : la rangée « Revoir la présentation », revenue — la grammaire de ses voisines (2 px, rayon 32, couleur du corps) */
#device #settingsScreen #replayPres,.frame #settingsScreen #replayPres{border-width:2px!important;border-style:solid!important;border-radius:32px!important;border-color:var(--c-creme95)!important}
#device.light #settingsScreen #replayPres,.frame.light #settingsScreen #replayPres{border-color:var(--c-brun09)!important}""")
io.open(f,'w',encoding='utf-8').write(S)
f='releve-aura.py'; S=io.open(f,encoding='utf-8').read()
rep("        CEDE, CEDE_TAU, RESISTE_TAU, PROF, REPOUSSE_TAU = 0.62, 0.05, 0.50, 0.46, 0.15\n        loi = lambda t: 1 - CEDE * math.exp(-t / CEDE_TAU) - (1 - CEDE) * math.exp(-t / RESISTE_TAU)\n        Gd = pg.evaluate(\"()=>{const G=_aura.G;return [G.CEDE,G.CEDE_TAU,G.RESISTE_TAU,G.PROF,G.REPOUSSE_TAU]}\")\n        if [(round(x, 4) if x is not None else None) for x in Gd] != [CEDE, CEDE_TAU, RESISTE_TAU, PROF, REPOUSSE_TAU]:",
"""        # ⚑ v139 (Tom, 9 oct. 2026, C-083) — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (original : sauvegardes/releve-aura-avant-v139.py) :
        #   « plus on appuie longtemps, plus ça s'enfonce : vite au début, puis de plus en plus lentement, jusqu'à une butée ; jamais de
        #   saut ; au relâcher, la fourrure revient lentement. » La loi d'avant (elle cède à 62 % en 50 ms, puis résiste) prenait un tiers
        #   de la profondeur à la première image. Nouvelle loi, en dur : profondeur q(t) = 1 − 1/(1 + t/0,60)², pression p = q^1,5 ;
        #   retour en 0,60 s. Le détail (chaque image, la vitesse, les sauts, la forme du contact) : redteam_enfonce.py.
        ENF_TAU, RETOUR_TAU, PROF = 0.60, 0.60, 0.46
        loi = lambda t: (1 - 1 / (1 + t / ENF_TAU) ** 2) ** 1.5
        Gd = pg.evaluate("()=>{const G=_aura.G;return [G.ENF_TAU,G.RETOUR_TAU,G.PROF]}")
        if [(round(x, 4) if x is not None else None) for x in Gd] != [ENF_TAU, RETOUR_TAU, PROF]:""")
rep("le toucher ne cède pas selon la loi : p = %s à 250 ms","le toucher ne s'enfonce pas selon la loi : p = %s à 250 ms")
rep("le creux ne RÉSISTE pas selon la loi : p = %s à 950 ms","le creux ne continue pas de s'enfoncer selon la loi : p = %s à 950 ms")
io.open(f,'w',encoding='utf-8').write(S)

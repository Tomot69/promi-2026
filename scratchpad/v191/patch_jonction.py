import io
p='app.html'; S=io.open(p,encoding='utf-8').read()
def rep(o,n):
    global S
    assert S.count(o)==1,(o[:80],S.count(o)); S=S.replace(o,n)
rep("""      try{ var g=c.getContext('2d'), E=c.width/(c.offsetWidth||390), px=g.getImageData(Math.round(4*E), Math.max(0, Math.round((mn-lw-6)*E)), 1, 1).data; f.champ='rgb('+px[0]+','+px[1]+','+px[2]+')'; }catch(_){ f.champ=null; } }
    return f; }""",
"""      try{ var g=c.getContext('2d'), E=c.width/(c.offsetWidth||390), px=g.getImageData(Math.round(4*E), Math.max(0, Math.round((mn-lw-6)*E)), 1, 1).data; f.champ='rgb('+px[0]+','+px[1]+','+px[2]+')'; }catch(_){ f.champ=null; }
      f.BAS=mx+lw/2; }
    /* ⚑ v191 (Tom, C-259 suite) — PROMI ET CHICHE : leur vague EST le trait du geste, et il fait exactement ce que fait la vague du Cercle, par ce même code. Ce qui
       change, et seulement ça : la ligne n'est pas un trait d'une couleur, c'est la ligne de la fiche — elle est retracée par SON peintre (`c.__ligne`, toutes ses
       couleurs, tous ses états) sur l'onde aplatie ; et son EMPREINTE (le haut de ce qu'elle peint, colonne par colonne, et son bas) se lit sur ce qu'elle peint
       (une fois par ouverture, hors de l'écran) : l'amorce effilée, la pointe, les points et les initiales débordent de la demi-épaisseur du trait. */
    else if(!f.cercle && c.__ligne && isFinite(base) && isFinite(amp) && window._onde && !d.classList.contains('dp-draft')){ var y2=window._onde.onde(base, amp), P2=[], mn2=1e9, mx2=-1e9; for(var x2=0;x2<=390;x2+=2){ var v2=y2(x2); P2.push(v2); if(v2<mn2) mn2=v2; if(v2>mx2) mx2=v2; }
      f.P=P2; f.min=mn2; f.max=mx2; f.s0=mn2-lw/2-J; f.base=base; f.amp=amp; f.ligne=c.__ligne;
      try{ var Ee=2, Hh=Math.ceil(mx2+60), o2=document.createElement('canvas'); o2.width=390*Ee; o2.height=Hh*Ee; var gg=o2.getContext('2d'); gg.setTransform(Ee,0,0,Ee,0,0); c.__ligne(gg, base, amp);
        var D2=gg.getImageData(0,0,o2.width,o2.height).data, n2=P2.length, EN2=[], bas2=-1e9, Wd=o2.width;
        for(var i3=0;i3<n2;i3++){ var top=1e9, xa=Math.max(0, (i3*2-1)*Ee), xb=Math.min(Wd-1, (i3*2+1)*Ee);
          for(var xx=xa;xx<=xb;xx++){ for(var yy=0;yy<o2.height;yy++){ if(D2[(yy*Wd+xx)*4+3]>8){ if(yy<top) top=yy; break; } }
            for(var yb=o2.height-1;yb>=0;yb--){ if(D2[(yb*Wd+xx)*4+3]>8){ if(yb/Ee>bas2) bas2=(yb+1)/Ee; break; } } }
          EN2.push(top<1e9 ? top/Ee : P2[i3]-lw/2); }
        f.EN=EN2; f.BAS=Math.max(bas2, mx2+lw/2); }catch(_){ f.EN=P2.map(function(v){ return v-lw/2; }); f.BAS=mx2+lw/2+16; }
      try{ var g3=c.getContext('2d'), E3=c.width/(c.offsetWidth||390), px3=g3.getImageData(Math.round(4*E3), Math.max(0, Math.round((mn2-lw-6)*E3)), 1, 1).data; f.champ=px3[3]>200 ? 'rgb('+px3[0]+','+px3[1]+','+px3[2]+')' : null; }catch(_){ f.champ=null; } }
    return f; }""")
rep("""    if(on && F && F.cercle && F.P && s>=F.s0) etat={t:Math.min(1, (s-F.s0)/COURSE)};   /* ⚑ v190 (Tom, C-259) : Promi et Chiche n'ont plus de trait à la jonction — leurs fiches sont celles de v188 */
    if(!etat){ if(montre){ montre=false; cv.style.setProperty('display','none','important'); } return; }""",
"""    if(on && F && F.P && s>=F.s0) etat={t:Math.min(1, (s-F.s0)/COURSE)};   /* ⚑ v191 (Tom, C-259 suite) : les trois natures (v190 : le Cercle seul) */
    geste(d, !!etat);
    if(!etat){ if(montre){ montre=false; cv.style.setProperty('display','none','important'); } return; }""")
rep("""    { var k=1-etat.t, Y=function(i){ return y0+(F.P[i]-F.min)*k; }, n=F.P.length, bas=F.max-s+F.lw/2+1.5;""",
"""    { var k=1-etat.t, Y=function(i){ return y0+(F.P[i]-F.min)*k; }, n=F.P.length, bas=F.BAS-s+1.5;""")
rep("""      g.beginPath(); for(var q=0;q<n;q++){ if(q) g.lineTo(q*2, Y(q)); else g.moveTo(0, Y(0)); } g.stroke();
      c.setAttribute('data-jonction', 'cercle,'+etat.t.toFixed(4)+','+(F.max-F.min).toFixed(2)); } }""",
"""      if(F.cercle){ g.beginPath(); for(var q=0;q<n;q++){ if(q) g.lineTo(q*2, Y(q)); else g.moveTo(0, Y(0)); } g.stroke(); }
      /* Promi, Chiche : la ligne de la fiche, par son peintre, sur l'onde (base', k·amp) — l'onde est linéaire en l'amplitude, c'est exactement y0 + (P − min)·k.
         Coupée net à la jonction, comme tout ce qui passe sous l'en-tête (avant de s'accrocher, l'amorce et la pointe y passent déjà). */
      else { g.save(); g.beginPath(); g.rect(0, J, 390, HT-J); g.clip(); try{ F.ligne(g, y0+k*(F.base-F.min), k*F.amp); }catch(_){ } g.restore(); }
      c.setAttribute('data-jonction', (F.cercle?'cercle':'fiche')+','+etat.t.toFixed(4)+','+(F.max-F.min).toFixed(2)); } }
  /* ⚑ v191 (Tom) — « Le geste ne marche qu'au repos, quand le trait est à sa place. Accroché ou aplati, un toucher sur lui fait défiler la fiche et ne trace rien. »
     La zone du geste ne prend plus le doigt tant que le trait est accroché : le doigt tombe sur la fiche, qui défile (aucune classe posée sur la fiche : une
     écriture de style sur la zone seule, rendue dès qu'il se décroche et à la fermeture). */
  var coupe=false;
  function geste(d, accroche){ accroche=!!(accroche && !cercle(d)); if(accroche===coupe) return; coupe=accroche; var z=document.getElementById('tenirZone'); if(!z) return;
    if(coupe) z.style.setProperty('pointer-events','none','important'); else z.style.removeProperty('pointer-events'); }""")
rep("""  (window._rangeurs=window._rangeurs||[]).push(function(){ F=null; if(montre && cv){ montre=false; cv.style.setProperty('display','none','important'); } });
})();""","""  (window._rangeurs=window._rangeurs||[]).push(function(){ F=null; geste(null, false); if(montre && cv){ montre=false; cv.style.setProperty('display','none','important'); } });
})();""")
rep("""window._v189Jonction=function(){ return {montre:montre, F:F?{s0:F.s0, min:F.min, max:F.max, lw:F.lw, cercle:F.cercle, P:F.P?F.P.slice():null, EN:F.EN?F.EN.slice():null}:null}; };""",
"""window._v189Jonction=function(){ return {montre:montre, coupe:coupe, F:F?{s0:F.s0, min:F.min, max:F.max, lw:F.lw, cercle:F.cercle, base:F.base, amp:F.amp, BAS:F.BAS, P:F.P?F.P.slice():null, EN:F.EN?F.EN.slice():null}:null}; };""")
rep("""jusqu'à sa place exacte de repos. ⚑ v190 (Tom) : PROMI ET CHICHE N'ONT PLUS DE TRAIT À LA JONCTION""","""jusqu'à sa place exacte de repos. ⚑ v191 : PROMI ET CHICHE AUSSI, leur vague étant le trait du geste (voir `forme`). ⚑ v190 (Tom) : PROMI ET CHICHE N'ONT PLUS DE TRAIT À LA JONCTION""")
rep("lot:'v190'","lot:'v191'")
io.open(p,'w',encoding='utf-8').write(S); print('ok')

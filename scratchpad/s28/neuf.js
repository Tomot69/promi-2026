 /* @F 23 SEPTEMBRE 2026, troisieme tour (Tom) — LE FOLIO : LES TITRES SUR DEUX LIGNES, LA
    GRILLE QUI S'ADAPTE, ET LA PELOTE DANS SON BLOC.
    LE DEFAUT, VU A LA CAPTURE : les titres etaient traces sur UNE ligne, centres, sans
    mesure et sans coupe — « le grand plongeoimonter la serre avant lesprendre l'arrosage
    autecuperer les plants de t… ». Quatre libelles se chevauchaient sur la meme rangee.
    CE QUI CHANGE, ET RIEN D'AUTRE :
      1 · un titre se MESURE (`measureText`) et se coupe aux MOTS, deux lignes au plus ;
          au-dela, points de suite sur la seconde. Jamais de reduction de taille (§6).
      2 · une rangee prend la hauteur de son titre LE PLUS HAUT — les rangees a une ligne
          ne s'espacent pas comme celles a deux. La hauteur totale se recalcule, et la
          planche reste centree.
      3 · LES TITRES LONGS SE REGROUPENT : on emet d'abord les une-ligne, puis les
          deux-lignes, chaque groupe dans son ordre. C'est le rangement qui coute le moins
          de hauteur — mesure : 5 rangees au lieu de 5, mais 2 rangees hautes au lieu de 4.
      4 · LE BLOC 2x2 porte LA PELOTE (`window.shPelote`), plus le Noyau : on ne partage
          plus son Noyau (Q284). Le mecanisme de reservation ne change pas — il etait deja
          ecrit pour deux cases sur deux, et il tient.
    @W RIEN NE SE SUPERPOSE, RIEN NE DISPARAIT : les quatre cases du bloc sont ENJAMBEES,
    les dalles se rangent autour dans l'ordre, et la planche compte `n + 4` cases. */
 var n=act.length;
 var cols=n<=6?2:(n<=12?3:(n<=24?4:5));
 var pad=W*0.075, gap=W*0.028;
 var cw=(W-pad*2-gap*(cols-1))/cols;
 var lab=Math.max(7,Math.round(cw*0.115));
 var LH=lab*1.28;                      /* l'interligne d'un titre */
 var SOUS=lab*1.5;                     /* la premiere ligne, sous la dalle */
 g.font='500 '+lab+'px Atkinson,Apfel,system-ui,sans-serif';
 /* — 1 · le titre, mesure puis coupe aux mots, deux lignes au plus — */
 function coupe(t){
   t=(t||'').trim(); if(!t) return [];
   if(g.measureText(t).width<=cw) return [t];
   var mots=t.split(/\s+/), l1='', i=0;
   while(i<mots.length){ var e=l1?l1+' '+mots[i]:mots[i];
     if(g.measureText(e).width>cw && l1) break; l1=e; i++; }
   var reste=mots.slice(i).join(' ');
   if(!reste) return [l1];
   if(g.measureText(reste).width<=cw) return [l1,reste];
   while(reste.length>1 && g.measureText(reste+'…').width>cw) reste=reste.slice(0,-1);
   return [l1, reste.replace(/\s+$/,'')+'…'];
 }
 var sansLab=(window.shLabels===false);
 var ITEMS=act.map(function(p){ var L=sansLab?[]:coupe(p.title);
   return {p:p, L:L, nl:Math.max(1,L.length)}; });
 /* — 3 · on regroupe : les une-ligne d'abord, les deux-lignes ensuite — */
 if(!sansLab){ var A=[],B=[];
   ITEMS.forEach(function(it){ (it.nl>1?B:A).push(it); });
   ITEMS=A.concat(B); }
 /* — 4 · le bloc de la Pelote : deux cases sur deux, enjambees — */
 var pel=!!window.shPelote, pelIdx=-1, skip={};
 if(pel&&cols>=2){
   var r0=Math.max(0,(window.shPelBR===undefined?1:window.shPelBR));
   var c0=Math.max(0,Math.min(cols-2,(window.shPelBC===undefined?0:window.shPelBC)));
   pelIdx=r0*cols+c0;
   skip[r0*cols+c0]=1; skip[r0*cols+c0+1]=1;
   skip[(r0+1)*cols+c0]=1; skip[(r0+1)*cols+c0+1]=1;
 }
 /* — on attribue les cases, puis on mesure chaque rangee — */
 var place=[], slot=0, maxSlot=0;
 for(var i=0;i<ITEMS.length;i++){
   while(skip[slot]) slot++;
   place.push(slot); if(slot>maxSlot) maxSlot=slot; slot++;
 }
 for(var k in skip){ var kk=+k; if(kk>maxSlot) maxSlot=kk; }
 var rows=Math.floor(maxSlot/cols)+1;
 /* — 2 · la hauteur d'une rangee suit son titre le plus haut — */
 var nlRow=[]; for(var r=0;r<rows;r++) nlRow.push(1);
 ITEMS.forEach(function(it,ix){ var r=Math.floor(place[ix]/cols);
   if(it.nl>nlRow[r]) nlRow[r]=it.nl; });
 var hRow=nlRow.map(function(nl){ return sansLab ? cw+lab*0.6 : cw+SOUS+(nl-1)*LH+lab*0.7; });
 var yRow=[], acc=0;
 for(var r2=0;r2<rows;r2++){ yRow.push(acc); acc+=hRow[r2]+gap; }
 var totH=acc-gap;
 var y0=Math.max(pad,(H-totH)/2);
 g.textAlign='center'; g.textBaseline='alphabetic';
 for(var i2=0;i2<ITEMS.length;i2++){
   var it2=ITEMS[i2], p=it2.p, s=place[i2];
   var x=pad+(s%cols)*(cw+gap), y=y0+yRow[Math.floor(s/cols)];
   var col=COL[p.status]||COL.encours;
   var tile=_dalleReelle(p.id);
   g.save(); g.translate(x+cw/2,y+cw/2);
   if(tile){ var rr=Math.min(cw/tile.width,cw/tile.height);
     var dw=tile.width*rr, dh=tile.height*rr;
     g.drawImage(tile,-dw/2,-dh/2,dw,dh);
   } else { var rd=cw*0.44; g.beginPath();
     g.moveTo(0,-rd);
     g.bezierCurveTo(rd*0.72,-rd*1.02,rd*1.04,-rd*0.42,rd*0.94,rd*0.16);
     g.bezierCurveTo(rd*0.86,rd*0.78,rd*0.32,rd*1.04,-rd*0.14,rd*0.96);
     g.bezierCurveTo(-rd*0.74,rd*0.86,-rd*1.04,rd*0.34,-rd*0.92,-rd*0.22);
     g.bezierCurveTo(-rd*0.82,-rd*0.76,-rd*0.42,-rd*0.98,0,-rd);
     g.closePath(); g.fillStyle=col; g.fill(); }
   g.restore();
   if(sansLab) continue;
   g.fillStyle=ink; g.globalAlpha=.82;
   g.font='500 '+lab+'px Atkinson,Apfel,system-ui,sans-serif';
   for(var li=0;li<it2.L.length;li++) g.fillText(it2.L[li], x+cw/2, y+cw+SOUS+li*LH);
   g.globalAlpha=1;
   _comp.push({id:p.id, mot:it2.L.join(' '), lignes:it2.L.length,
               x:Math.round(x), y:Math.round(y), cw:Math.round(cw), lab:Math.round(lab*10)/10});
 }
 window._plancheComp={n:_comp.length, mots:_comp.map(function(c){return c.mot;}),
                      cases:_comp, noyau:false, pelote:pel,
                      rangees:nlRow.slice(), cols:cols};
 /* — la Pelote dans son bloc — */
 if(pel&&pelIdx>=0){
   var nr=Math.floor(pelIdx/cols), nc=pelIdx%cols;
   var bx=pad+nc*(cw+gap), by=y0+yRow[nr];
   var bw=cw*2+gap, bh=(hRow[nr]||cw)+gap+(hRow[nr+1]||hRow[nr]||cw);
   var D=Math.round(Math.min(bw,bh)*0.92);
   try{
     var src=window._aura&&window._aura.pelote?window._aura.pelote():null;
     if(src&&src.width) g.drawImage(src, bx+(bw-D)/2, by+(bh-D)/2, D, D);
   }catch(e){}
 }

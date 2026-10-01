var KD=[4.7,5.3,4.1,0.6,1.9,1.1, 6.7,5.9,7.3,2.4,0.7,1.5];
var PIDS=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18];
window.addEventListener('load',function(){
  /* ⚑ ON AGRANDIT LA TOILE AVANT DE RELEVER SES DALLES.
     seedGray() ne repeuple que si la Toile est vide : on l'amorce petite, puis
     on agrandit le canevas et relax() etale les memes cellules. Les dalles
     passent de 70 a 200-380 px, AU PAS ABSOLU INCHANGE — assez grandes pour
     couvrir une cellule sans jamais qu'on ait a les repeter. */
  try{
    Toile_resize(); Toile.sync(PIDS);
    var ho=document.getElementById('toileCv'), pa=ho.parentNode;
    pa.style.width='1500px'; pa.style.height='2100px';
    ho.style.width='1500px'; ho.style.height='2100px';
    Toile_resize(); Toile.sync(PIDS);
  }catch(e){}
  setTimeout(function(){
    window.__moteur=!!(window.Toile&&window.Toile.mondeCourant);
    /* 77 cellules : la taille de dalle mesuree sur la Toile */
    var S=sites(77,KD), CEL=[], i;
    for(i=0;i<S.length;i++) CEL.push(cellule(S,i,0.020));
    /* la grappe des Promi : la ou ils se sont plantes */
    var cv0=Math.cos(2.9), sv0=Math.sin(2.9), ct0=Math.cos(0.32), st0=Math.sin(0.32);
    var v=[-0.10,-0.14,0.985];
    var zp=-v[1]*st0+v[2]*ct0, yy=v[1]*ct0+v[2]*st0;
    var F=nrm([v[0]*cv0-zp*sv0, yy, v[0]*sv0+zp*cv0]);
    /* ⚑ TOUTES LES CELLULES PORTENT LEUR DALLE — c'est ce qui fait la BOULE.
       Laisser des cellules vides creusait la silhouette : la sphere n'etait
       plus ronde, c'etait l'union des dalles plantees. Le vide qu'on veut voir,
       c'est le JOINT entre deux dalles, pas un trou dans la boule. */
    var PL=[];
    for(i=0;i<S.length;i++) PL.push(1);
    /* le coton : 110 000 touffes de trois brins, peignees par un champ lisse */
    var FIB=semisFibres(190000);
    var ATF=atlasFibres([3.4,4.4,5.6], 24);
    var G=document.getElementById('g'), infos=[];
    var MONDES=['encre','mosaique','touffe','braille','pixel','terrazzo','gravure','sillons'];
    var NOM={encre:'Encre',mosaique:'Mosaïque',touffe:'Touffe',braille:'Braille',
             pixel:'Pixel',terrazzo:'Terrazzo',gravure:'Gravure',sillons:'Sillons'};
    MONDES.forEach(function(m){
      try{ Toile.setTheme(m); }catch(e){}
      var DAL=[];
      for(var p=0;p<PIDS.length;p++){
        var c=document.createElement('canvas');
        try{ Toile.dalleTrame(c, PIDS[p], 1); }catch(e){}
        if(c.width>8) DAL.push(c);
      }
      var fg=document.createElement('figure');
      var box=document.createElement('div'); box.className='cadre';
      var cv=document.createElement('canvas'); cv.setAttribute('data-cad','m-'+m);
      box.appendChild(cv); fg.appendChild(box);
      var fc=document.createElement('figcaption'); fc.innerHTML='<b>'+NOM[m]+'</b>';
      fg.appendChild(fc); G.appendChild(fg);
      infos.push(peint(cv,{css:470,R:0.425,lac:2.9,tan:0.32,
        sites:S, cells:CEL, dalles:DAL, plant:PL, rond:7,
        fibres:FIB, atlasFib:ATF, oriFib:24, taiFib:3}));
    });
    window.__infos=infos; window.__pret=true;
  },900);
});

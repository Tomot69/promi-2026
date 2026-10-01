#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LOT · LA RÉCIPROCITÉ SUR L'AURA (chantier 79, Tom 14 sept. 2026 : B avec C). assert == 1.
import io
p = 'app.html'; S = io.open(p, encoding='utf-8').read()


def R(a, b, n=1):
    global S
    c = S.count(a); assert c == n, (c, a[:90]); S = S.replace(a, b)


# ── 1 · LES DONNÉES : ce qu'on te tient (Q215 · 1) ──
R("""  function donnees(){
    var P=mesPromi(), T=ordreTenus(P);
    return {P:P, T:T, n:T.length, nature:natureMaj(T), toi:parts(P), gens:personnes(P)};
  }""",
"""  /* ⚑ CE QU'ON TE TIENT (Q215, Tom 14 sept.) — ce qu'une personne te promet à toi, sa moitié d'un Chiche relevé avec toi, ce
     qu'elle promet à une de tes Nuées. Celui qui tient déclare, tu reçois : on lit son état, on ne le décide jamais. */
  function envers(){
    var out=[];
    tous().forEach(function(p){ if(!p || p.draft || p.req) return;
      var de=(p.from && p.from!=='moi' && !estMoi(p.from)) ? p.from : null;
      var aMoi=(!p.who || p.who==='moi' || estMoi(p.who));
      if(de && (aMoi || (p.nuee && typeof NUE!=='undefined' && NUE[p.nuee]))) out.push({nom:de, p:p});
      else if(!de && p.chiche && p.chicheEtat==='releve' && p.avec && !estMoi(p.avec)) out.push({nom:p.avec, p:p});
    });
    return out;
  }
  /* ⚑ LA RANGÉE : qui te promet sans que tu lui promettes y entre aussi (Q215 · 3). ORDRE ALPHABÉTIQUE, jamais par valeur. */
  function gensRecip(P, E){
    var m={}; personnes(P).forEach(function(g){ m[g.nom]=g.parts; });
    var r={}; E.forEach(function(x){ if(x.nom==='le groupe') return; (r[x.nom]=r[x.nom]||[]).push(x.p); });
    return Object.keys(m).concat(Object.keys(r).filter(function(n){ return !m[n]; }))
      .sort(function(a,b){ return a.localeCompare(b,'fr'); })
      .map(function(n){ return {nom:n, parts:m[n]||null, recu:r[n]?parts(r[n]):null}; });
  }
  function donnees(){
    var P=mesPromi(), T=ordreTenus(P), E=envers();
    var RT=E.filter(function(x){ return x.p.status==='tenu'; }).map(function(x){ return x.p; }).sort(function(a,b){ return a.id-b.id; });
    return {P:P, T:T, n:T.length, nature:natureMaj(T), toi:parts(P), gens:gensRecip(P,E), recu:E.length?parts(E.map(function(x){ return x.p; })):null, RT:RT};
  }""")

# ── 2 · LE NOYAU : deux moitiés (§2.9 corrigé) ──
R("""  function noyau(dia, ep, dph, pa, nom, moi){""", """  function noyau(dia, ep, dph, pa, nom, moi, recu){""")
R("""    arc('au-piste', null, 1, 0);
    var an=-90, GA=2.6;
    for(var z=0; z<3; z++){ var pc=pa[z]*100; if(pc>GA) arc('au-arc', ETA[z][1], (pc-GA)/100, an); an+=pc*3.6; }
    box.appendChild(s);""",
"""    /* ⚑ LES DEUX MOITIÉS (Tom, 14 sept. 2026 — le §2.9 corrigé) : à GAUCHE ce que tu tiens envers la personne, à DROITE ce
       qu'elle te tient. La grammaire du trait : ta moitié à gauche, celle de l'autre à droite. Les deux partent de midi, en
       miroir, séparées par un JOUR de 6 px en haut et en bas. Une moitié absente ne se peint pas — ni piste, ni vide.
       Mesuré : « seulement lui → moi » ne se superpose jamais à « seulement moi → lui » (IoU 0,01). */
    var JOUR=6, g=(JOUR/2)/r*180/Math.PI, TOT=180-2*g, GA=2.6/100*TOT;
    function pt(a){ var t=(a-90)*Math.PI/180; return (cx+r*Math.cos(t)).toFixed(2)+' '+(cx+r*Math.sin(t)).toFixed(2); }
    function seg(par, a0, a1, col, cls){ if(a1-a0<=0.3) return; var e=svg('path');
      e.setAttribute('d','M'+pt(a0)+' A'+r+' '+r+' 0 '+((a1-a0)>180?1:0)+' 1 '+pt(a1)); e.setAttribute('fill','none');
      e.setAttribute('stroke',col); e.setAttribute('stroke-width',ep); e.setAttribute('stroke-linecap','butt'); e.setAttribute('class',cls); par.appendChild(e); }
    function somme(x){ return x ? (x[0]+x[1]+x[2]) : 0; }
    function moitie(par, parts, cote){
      var n=[0,1,2].filter(function(z){ return parts[z]>0; }).length, a=(cote==='d') ? g : 360-g;
      for(var z=0; z<3; z++){ var v=parts[z]; if(v<=0) continue; var L=v*TOT-(n>1?GA:0);
        if(cote==='d'){ seg(par, a, a+L, ETA[z][1], 'au-arc'); a+=v*TOT; } else { seg(par, a-L, a, ETA[z][1], 'au-arc'); a-=v*TOT; } }
    }
    if(somme(pa)>0) moitie(s, pa, 'g');
    if(somme(recu)>0){ var gr=svg('g'); gr.setAttribute('class','au-recu'); moitie(gr, recu, 'd'); s.appendChild(gr); w.setAttribute('data-recu','1'); }
    box.appendChild(s);""")
R("""      NX.appendChild(noyau(K.toi.d, K.toi.arc, K.toi.ph, D.toi, 'toi', true));
      var gp=el('div','au-gp');
      D.gens.forEach(function(g){ gp.appendChild(noyau(K.pers.d, K.pers.arc, K.pers.ph, g.parts, g.nom, false)); });""",
"""      NX.appendChild(noyau(K.toi.d, K.toi.arc, K.toi.ph, D.toi, 'toi', true, D.recu));
      var gp=el('div','au-gp');
      D.gens.forEach(function(g){ gp.appendChild(noyau(K.pers.d, K.pers.arc, K.pers.ph, g.parts, g.nom, false, g.recu)); });""")

# ── 3 · LA RANGÉE « CE QU'ON T'A TENU » ──
R("""    GR=el('div','au-gr'); MO.appendChild(GR); CAD.appendChild(MO);""",
"""    GR=el('div','au-gr'); MO.appendChild(GR); CAD.appendChild(MO);
    /* ⚑ CE QU'ON T'A TENU (Q215) — le miroir de « Ce que tu as tenu ». En gratuit : visible, flouté à 2,4 px, l'encart net
       posé dessus. On voit qu'il existe une autre moitié, jamais ce qu'elle contient. */
    MO2=el('div','au-mo au-mo2'); MO2.appendChild(el('h3',null,'Ce qu’on t’a tenu'));
    var z2=el('div','au-zone2'); GR2=el('div','au-gr au-gr2'); z2.appendChild(GR2);
    ENC2=el('div','au-enc2'); ENC2.setAttribute('role','button'); ENC2.appendChild(el('span',null,'✦ Le Cercle'));
    ENC2.addEventListener('click', function(ev){ ev.stopPropagation(); try{ var pl=document.getElementById('plusScreen'); if(pl) pl.classList.add('show'); }catch(_){} });
    z2.appendChild(ENC2); MO2.appendChild(z2); CAD.appendChild(MO2);""")
R("""    var L=D.T.slice(-nbMoisson()).reverse();
    L.forEach(function(p){ GR.appendChild(cellule(p)); });""",
"""    var L=D.T.slice(-nbMoisson()).reverse();
    L.forEach(function(p){ GR.appendChild(cellule(p)); });
    GR2.textContent='';
    var L2=D.RT.slice(-3).reverse(); L2.forEach(function(p){ GR2.appendChild(cellule(p)); });
    MO2.classList.toggle('au-sans', vide || !L2.length);
    voile();""")
R("""    if(!GR) return;
    [].forEach.call(GR.querySelectorAll('canvas[data-pid]'), function(cv){""",
"""    if(!GR) return;
    [].forEach.call(CAD.querySelectorAll('.au-gr canvas[data-pid]'), function(cv){""")
R("""      var bas = MO.classList.contains('au-sans') ? c.lg+K.lgH : c.mo+MO.offsetHeight;""",
"""      var bas = MO.classList.contains('au-sans') ? c.lg+K.lgH : c.mo+MO.offsetHeight;
      /* la seconde rangée suit la première du même air (28) */
      c.mo2 = bas + K.AIR; if(MO2 && !MO2.classList.contains('au-sans')) bas = c.mo2 + MO2.offsetHeight;""")
R("""    var k=[c.nx,c.lg,c.mo,c.bt,c.fin].map(function(v){ return v.toFixed(2); }).join('|');""",
"""    if(c.mo2==null) c.mo2=c.mo;
    var k=[c.nx,c.lg,c.mo,c.mo2,c.bt,c.fin].map(function(v){ return v.toFixed(2); }).join('|');""")
R("""    [[NX,c.nx],[LG,c.lg],[MO,c.mo],[BT,c.bt],[FIN,c.fin-1]].forEach(function(a){""",
"""    [[NX,c.nx],[LG,c.lg],[MO,c.mo],[MO2,c.mo2],[BT,c.bt],[FIN,c.fin-1]].forEach(function(a){ if(!a[0]) return;""")
# les variables et le voile
R("""  function cellule(p){""",
"""  var MO2=null, GR2=null, ENC2=null;
  /* le voile suit le Cercle : une classe que le code pose (§8), comparée avant d'écrire */
  function voile(){ if(!CAD) return; var dv=document.getElementById('device'); var v=!(dv && dv.classList.contains('premium'));
    if(CAD.classList.contains('au-voile')!==v) CAD.classList.toggle('au-voile', v); }
  try{ var _dv=document.getElementById('device'); if(_dv) new MutationObserver(voile).observe(_dv,{attributes:true,attributeFilter:['class']}); }catch(_){}
  function cellule(p){""")
R("""      toi:D.toi, gens:D.gens.map(function(g){ return {nom:g.nom, parts:g.parts}; }),""",
"""      toi:D.toi, recu:D.recu, gens:D.gens.map(function(g){ return {nom:g.nom, parts:g.parts, recu:g.recu}; }),
      onTaTenu:D.RT.slice(-3).reverse().map(function(p){ return p.id; }),""")

# ── 4 · LE JEU : trois promesses reçues (titres de Tom, 14 sept.) ──
R("""      pousse(P('rapporter le livre','Rachel',14,2,'tenu',null));""",
"""      pousse(P('rapporter le livre','Rachel',14,2,'tenu',null));

      /* ⚑ TROIS PROMESSES REÇUES — titres de Tom, 14 sept. 2026 (Q215) : ce qu'un proche te promet, à toi seul.
         « Rachel te promet de t'apprendre à nager » · « Nico te promet de rapporter la perceuse » · « Marion te promet de venir dimanche ». */
      pousse(P("t'apprendre à nager",'moi',7,2,'encours',null,'Rachel'));
      pousse(P('rapporter la perceuse','moi',5,2,'tenu',null,'Nico'));
      pousse(P('venir dimanche','moi',3,2,'rate',null,'Marion'));""")

# ── 5 · la carte dit « de Rachel », pas « à moi » ──
R("""    if(!w || w.toLowerCase()==='moi') return 'à moi';""",
"""    if((!w || w.toLowerCase()==='moi') && p.from && p.from!=='moi') return 'de '+p.from;   /* une promesse reçue */
    if(!w || w.toLowerCase()==='moi') return 'à moi';""")

CSS = r"""<style id="lot-RECIPROCITE-css">
/* ⚑ CE QU'ON T'A TENU + LE VOILE (Q215). La rangée reprend « Ce que tu as tenu » à l'identique. */
#auraScreen.au2 .au-zone2{position:relative}
#auraScreen.au2 .au-enc2{display:none}
#auraScreen.au2 .au-voile .au-recu{filter:blur(2.4px)}
#auraScreen.au2 .au-voile .au-gr2{filter:blur(2.4px);pointer-events:none}
#auraScreen.au2 .au-voile .au-enc2{display:flex;position:absolute;left:0;right:0;top:50%;height:90px;transform:translateY(-50%);z-index:3;
  border-radius:26px;align-items:center;justify-content:center;cursor:pointer;background:#F4EEE1}
#device.light #auraScreen.au2 .au-voile .au-enc2,.frame.light #auraScreen.au2 .au-voile .au-enc2{background:#16171B}
#auraScreen.au2 .au-enc2 span{font-family:Bricolage,system-ui,sans-serif;font-weight:700;font-size:22px;letter-spacing:-.02em;color:#8A5CF0;-webkit-text-fill-color:#8A5CF0;white-space:nowrap}
#device.light #auraScreen.au2 .au-enc2 span,.frame.light #auraScreen.au2 .au-enc2 span{color:#CBAAFF;-webkit-text-fill-color:#CBAAFF}
</style>
"""
S = S.replace('</body>', CSS + '</body>', 1)
io.open(p, 'w', encoding='utf-8').write(S)
print('lot réciprocité appliqué')

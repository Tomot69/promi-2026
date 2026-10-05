import io
S=io.open('scratchpad/v129/dessin/ov.js',encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n, (S.count(a), a[:60]); S=S.replace(a,b)
rep("/* PLANCHE v127 (C-042) — posé PAR-DESSUS l'app par le script de planche, jamais dans l'app. */",
    "/* PLANCHE v130 (C-042) — posé PAR-DESSUS l'app par le script de planche, jamais dans l'app. Rangée A SOUS le trait, déploiements SOUS la rangée ; rien dans la bande. */")
# les outils se déclarent (preuve de non-superposition)
rep("function disque(x, y, ic, enc, inv, sel, d, bord){ d=d||44; return el(", "function disque(x, y, ic, enc, inv, sel, d, bord){ d=d||44; return outil(el(")
rep("justify-content:center;color:'+(sel?inv:enc)+';background:'+(sel?enc:'transparent'), ic); }", "justify-content:center;color:'+(sel?inv:enc)+';background:'+(sel?enc:'transparent'), ic)); }\n  function outil(e){ e.setAttribute('data-ov-outil','1'); return e; }")
rep("o.appendChild(el('left:'+(366-104)+'px;top:'+y+'px;width:104px;height:44px;border-radius:22px;background:'+enc+';display:flex;align-items:center;justify-content:center', mot('Poser', inv)));",
    "o.appendChild(outil(el('left:'+(366-104)+'px;top:'+y+'px;width:104px;height:44px;border-radius:22px;background:'+enc+';display:flex;align-items:center;justify-content:center', mot('Poser', inv))));")
# les tailles : SOUS la rangée, alignées sur l'outil choisi
rep("x=c.xOutil[c.sel]||24, y=c.yOutils-54;", "x=c.xOutil[c.sel]||24, y=c.yOutils+54;")
rep("p.appendChild(h); }); o.appendChild(p); }", "p.appendChild(h); }); o.appendChild(outil(p)); }")
rep("border:2px solid '+enc+';background:'+fond); o.appendChild(p);\n    ['TRAIT','FOND']", "border:2px solid '+enc+';background:'+fond); o.appendChild(outil(p));\n    ['TRAIT','FOND']")
# les vraies couleurs de l'app : le corps est LU sur la fiche, l'encre suit sa clarté
rep("c.corps=c.light?'#F7F0DE':CORPS[c.nat]; c.encCorps=c.light?'#201908':'#F7F0DE';",
    "var _bg=(getComputedStyle(document.getElementById('detailPoster')).backgroundColor.match(/[\\d.]+/g)||[247,240,222]).map(Number); c.corps='rgb('+_bg[0]+','+_bg[1]+','+_bg[2]+')'; c.encCorps=((0.2126*_bg[0]+0.7152*_bg[1]+0.0722*_bg[2])>128)?'#201908':'#F7F0DE';")
# v130 : la page se réorganise
rep("    if(c.cachePhoto){", """    if(c.cacheSel){ c.cacheSel.forEach(function(s){ [].forEach.call(document.querySelectorAll(s), function(e){ e.setAttribute('data-ov-cache','1'); e.style.visibility='hidden'; }); }); }
    if(c.descendSel){ c.descendSel[0].forEach(function(s){ [].forEach.call(document.querySelectorAll(s), function(e){ e.setAttribute('data-ov-tr', e.style.transform||''); e.setAttribute('data-ov-dy','1'); e.style.setProperty('transform','translateY('+c.descendSel[1]+'px)','important'); }); }); }
    if(c.seulTitre){ var P=document.getElementById('detailPoster'), dv=document.getElementById('device').getBoundingClientRect(), ti=document.getElementById('dptTitre');
      [].forEach.call(P.querySelectorAll('*'), function(e){ if(e===ti||e.contains(ti)||ti.contains(e)) return; if(e.closest('#dpDetails')) return; var r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return; if(e.tagName==='CANVAS'&&e.id==='dpTrameCv') return;
        if(r.top-dv.top>=c.seulTitre[0]-1 && e.children.length===0 || (e.tagName==='CANVAS'&&r.top-dv.top>=c.seulTitre[0]-1)){ e.setAttribute('data-ov-cache','1'); e.style.visibility='hidden'; } });
      [].forEach.call(P.querySelectorAll('*'), function(e){ if(e===ti||e.contains(ti)||ti.contains(e)||e.closest('#dpDetails')||e.id==='dpTrameCv') return; var r=e.getBoundingClientRect(), cs=getComputedStyle(e); if(r.top-dv.top>=c.seulTitre[0]-1 && r.bottom-dv.top<=762 && (parseFloat(cs.borderTopWidth)>0 || (cs.backgroundColor!=='rgba(0, 0, 0, 0)' && cs.backgroundColor!==getComputedStyle(P).backgroundColor) || cs.backgroundImage!=='none')){ e.setAttribute('data-ov-cache','1'); e.style.visibility='hidden'; ti.style.visibility='visible'; } });
      ti.setAttribute('data-ov-tr', ti.style.transform||''); ti.setAttribute('data-ov-dy','1'); ti.style.setProperty('transform','translateY('+c.seulTitre[1]+'px)','important'); }
    if(c.cachePhoto){""")
rep("e.style.transform=e.getAttribute('data-ov-tr')||''; e.removeAttribute('data-ov-dy'); });", "e.style.removeProperty('transform'); if(e.getAttribute('data-ov-tr')) e.style.transform=e.getAttribute('data-ov-tr'); e.removeAttribute('data-ov-dy'); });")
rep("  return {montre:montre, nettoie:nettoie};", """  function preuve(){ var dv=document.getElementById('device').getBoundingClientRect(), L=[].map.call(document.querySelectorAll('#ovC042 [data-ov-outil]'), function(e){ var r=e.getBoundingClientRect(); return [r.top-dv.top, r.bottom-dv.top]; });
    return {n:L.length, haut:Math.min.apply(null,L.map(function(x){return x[0];})), bas:Math.max.apply(null,L.map(function(x){return x[1];}))}; }
  return {montre:montre, nettoie:nettoie, preuve:preuve};""")
io.open('scratchpad/v131/dessin/ov.js','w',encoding='utf-8').write(S)
S=io.open('scratchpad/v131/dessin/ov.js',encoding='utf-8').read()
n=S.count("e.style.visibility='hidden';"); assert n>=4, n
S=S.replace("e.style.visibility='hidden';","e.style.setProperty('visibility','hidden','important');")
S=S.replace("ti.style.visibility='visible'; } });","ti.style.setProperty('visibility','visible','important'); } });")
rep_a="r.bottom-dv.top<=762 && (parseFloat"; assert S.count(rep_a)==1; S=S.replace(rep_a,"r.top-dv.top<760 && (parseFloat")
a="e.style.visibility=''; e.removeAttribute('data-ov-cache');"; assert S.count(a)==1; S=S.replace(a,"e.style.removeProperty('visibility'); e.removeAttribute('data-ov-cache');")
io.open('scratchpad/v131/dessin/ov.js','w',encoding='utf-8').write(S)
# ── v131 : déploiements compacts (8 pt sous la rangée, panneau de 114), le Cercle descend d'un bloc
S=io.open('scratchpad/v131/dessin/ov.js',encoding='utf-8').read()
def r2(a,b):
    global S
    assert S.count(a)==1,(S.count(a),a[:60]); S=S.replace(a,b)
r2("x=c.xOutil[c.sel]||24, y=c.yOutils+54;","x=c.xOutil[c.sel]||24, y=c.yOutils+52;")
r2("y=c.yRow+54, P=c.palette","y=c.yRow+52, P=c.palette")
r2("width:342px;height:128px;border-radius:30px;border:2px solid '+enc+';background:'+fond); o.appendChild(outil(p));","width:342px;height:114px;border-radius:30px;border:2px solid '+enc+';background:'+fond); o.appendChild(outil(p));")
r2("p.appendChild(el('left:'+(10+i*161)+'px;top:10px;width:157px;height:44px;","p.appendChild(el('left:'+(8+i*163)+'px;top:6px;width:159px;height:44px;")
r2("d=el('left:'+(16+i*64)+'px;top:66px;width:44px;height:44px;","d=el('left:'+(16+i*64)+'px;top:58px;width:44px;height:44px;")
r2("p.appendChild(el('left:'+(16+i*64-5)+'px;top:61px;width:54px;height:54px;","p.appendChild(el('left:'+(16+i*64-4)+'px;top:54px;width:52px;height:52px;")
r2("    if(c.cachePhoto){ [].forEach","""    if(c.bloc){ [].forEach.call(document.querySelectorAll(c.bloc[0]), function(e){ e.setAttribute('data-ov-tr', e.style.transform||''); e.setAttribute('data-ov-dy','1'); e.style.setProperty('transform','translateY('+c.bloc[1]+'px)','important'); }); }
    if(c.cachePhoto){ [].forEach""")
io.open('scratchpad/v131/dessin/ov.js','w',encoding='utf-8').write(S)

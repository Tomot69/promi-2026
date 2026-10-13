#!/usr/bin/env python3
"""v145 (C-118) — relève, sur l'app réelle (banc_tom, WebKit @3x), la fiche AVANT le geste et la fiche TENUE, élément par élément (place, police,
couleur, texte, canevas), pour un Promi et un Chiche, en clair et en sombre : la matière des pages de variantes. Écrit variantes/tenir-donnees.js."""
import sys, json, io, base64; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
SNAP = r"""()=>{ var dv=document.getElementById('device'), d=dv.getBoundingClientRect(), k=d.width/390, dp=document.getElementById('detailPoster'), out=[];
  function rect(e){ var r=e.getBoundingClientRect(); return [ +((r.left-d.left)/k).toFixed(2), +((r.top-d.top)/k).toFixed(2), +(r.width/k).toFixed(2), +(r.height/k).toFixed(2) ]; }
  function vu(e){ var cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity<0.05) return false; var r=e.getBoundingClientRect(); return r.width>1&&r.height>1&&r.bottom>d.top&&r.top<d.bottom&&r.right>d.left&&r.left<d.right; }
  function cache(e){ for(var n=e; n && n!==dv; n=n.parentElement){ var cs=getComputedStyle(n); if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity<0.05) return true; } return false; }
  var all=[dp].concat([].slice.call(dp.querySelectorAll('*')));
  all.forEach(function(e,i){ if(cache(e)||!vu(e)) return; var cs=getComputedStyle(e), tag=e.tagName.toLowerCase();
    var txt=[].filter.call(e.childNodes,function(n){return n.nodeType===3&&n.nodeValue.trim();}).map(function(n){return n.nodeValue.replace(/\s+/g,' ');}).join('');
    var bg=cs.backgroundColor, aFond=!/rgba?\(0, 0, 0, 0\)|transparent/.test(bg), bord=parseFloat(cs.borderTopWidth)||0;
    var o={i:i, id:e.id||'', cls:(typeof e.className==='string'?e.className:'').slice(0,80), tag:tag, r:rect(e)};
    if(tag==='canvas'){ try{ o.img=e.toDataURL('image/png'); o.cw=e.width; o.ch=e.height; }catch(_){ } ['data-trait','data-matiere','data-matiere-base','data-champ','data-mini'].forEach(function(a){ if(e.getAttribute(a)!=null) o[a]=e.getAttribute(a); }); out.push(o); return; }
    if(tag==='svg'){ o.svg=e.outerHTML; o.col=cs.color; out.push(o); return; }
    if(e.closest('svg')) return;
    if(!txt && !aFond && !bord) return;
    if(txt){ o.txt=txt; var rg=document.createRange(); rg.selectNodeContents(e); var q=rg.getBoundingClientRect(); o.enc=[ +((q.left-d.left)/k).toFixed(2), +((q.top-d.top)/k).toFixed(2), +(q.width/k).toFixed(2), +(q.height/k).toFixed(2) ];
      o.f={fam:cs.fontFamily, fs:parseFloat(cs.fontSize), fw:cs.fontWeight, ls:cs.letterSpacing, tt:cs.textTransform, lh:cs.lineHeight, ta:cs.textAlign, col:cs.color, fill:cs.webkitTextFillColor, st:cs.fontStyle, ws:cs.whiteSpace}; }
    if(aFond) o.bg=bg; if(bord){ o.bd=[bord, cs.borderTopColor, cs.borderTopStyle]; } var br=parseFloat(cs.borderTopLeftRadius)||0; if(br) o.br=br; if(cs.transform&&cs.transform!=='none') o.tr=cs.transform;
    out.push(o); });
  return {cls:dp.className, corps:getComputedStyle(dp).backgroundColor, els:out}; }"""
def dalle(pg, pid, nat):
    """la dalle seule, rendue par le moteur à la taille que la fiche lui donne maintenant (la boîte déclarée par le peintre), teinte comme la bande"""
    return pg.evaluate("""([pid,nat])=>{ try{ var cv=document.getElementById('dpTrameCv'), m=(cv.getAttribute('data-matiere')||'').split(',').map(Number), b=(cv.getAttribute('data-matiere-base')||'').split(',').map(Number);
        var kx=cv.width/(b[0]||cv.width), o=window._ppRampe?{rampe:window._ppRampe(nat)}:undefined, c=window._rendDalle(pid, Math.round(m[2]*kx), Math.round(m[3]*kx), o, true);
        var cnv=c&&(c.cv||c.canvas||c); return {boite:m, base:b, cw:cv.width, ch:cv.height, img:(cnv&&cnv.toDataURL)?cnv.toDataURL('image/png'):null, w:cnv&&cnv.width, h:cnv&&cnv.height}; }catch(e){ return {err:String(e)}; } }""", [pid, nat])
OUT = {}
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        ctx = B.contexte(b, sombre=sombre); pg = B.ouvre(ctx)
        B.plante_doigt(pg, 'rendre le livre', 'moi', 0); B.plante_doigt(pg, 'écrire à Lou', 'Rachel', 0); B.plante_doigt(pg, 'le grand plongeoir', 'moi', 1); B.plante_doigt(pg, 'arroser le ficus', 'moi', 0)
        P = pg.evaluate("()=>promises.map(p=>({id:p.id,title:p.title,who:p.who,chiche:!!p.chiche,status:p.status}))")
        for nat, titre in (('promi', 'écrire à Lou'), ('chiche', 'le grand plongeoir')):
            pid = [x for x in P if x['title'] == titre][0]['id']; cle = nat + ('-sombre' if sombre else '-clair'); E = {}
            pg.evaluate("()=>{ closeAll(); }"); pg.wait_for_timeout(900); pg.evaluate("id=>{ openDetail(id); }", pid); pg.wait_for_timeout(3200)
            E['avant'] = pg.evaluate(SNAP); E['avant']['dalle'] = dalle(pg, pid, nat); B.capture(pg, 'scratchpad/v145/extrait/%s-avant.png' % cle)
            pg.evaluate("()=>{ var b=document.querySelector('#segStatus button[data-st=\"tenu\"]'); b&&b.click(); }"); pg.wait_for_timeout(900)
            E['instant'] = pg.evaluate(SNAP); E['instant']['dalle'] = dalle(pg, pid, nat); B.capture(pg, 'scratchpad/v145/extrait/%s-instant.png' % cle)
            pg.wait_for_timeout(1500); E['juste'] = pg.evaluate(SNAP); B.capture(pg, 'scratchpad/v145/extrait/%s-juste.png' % cle)
            pg.wait_for_timeout(3600); E['tenue'] = pg.evaluate(SNAP); E['tenue']['dalle'] = dalle(pg, pid, nat); B.capture(pg, 'scratchpad/v145/extrait/%s-tenue.png' % cle)
            OUT[cle] = E
            for k in ('avant', 'instant', 'juste', 'tenue'):
                print(cle, k, '|', E[k]['cls'][:70], '| corps', E[k]['corps'], '|', len(E[k]['els']), 'éléments', '| dalle', (E[k].get('dalle') or {}).get('boite'), (E[k].get('dalle') or {}).get('err'), flush=True)
        ctx.close()
    b.close()
io.open('scratchpad/v145/extrait/fiches.json', 'w', encoding='utf-8').write(json.dumps(OUT, ensure_ascii=False))

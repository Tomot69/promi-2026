import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
ETAT = """()=>{ var d=document.getElementById('detailPoster'), a=document.activeElement, inp=document.getElementById('dCommentInput'); var r=inp?inp.getBoundingClientRect():null, dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390;
  return {cls:d.className.replace(/\\s+/g,' ').slice(0,120), actif:(a&&(a.id||a.tagName)), input:r?[Math.round((r.left-dv.left)/k),Math.round((r.top-dv.top)/k),Math.round(r.width/k),Math.round(r.height/k)]:null, vis:inp?getComputedStyle(inp).visibility+'/'+getComputedStyle(inp).display:null,
          comm:(cur&&cur.comments||[]).map(c=>c.by+': '+c.t), blocs:[...document.querySelectorAll('#detailPoster .cm-block, #detailPoster .cm-row, #detailPoster .cm-line')].length, carte:(function(){ var m=document.getElementById('dpMsg'); if(!m) return null; var q=m.getBoundingClientRect(); return [Math.round((q.top-dv.top)/k), Math.round(q.height/k), m.textContent.trim().slice(0,60), getComputedStyle(m.parentNode).display]; })()}; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx)
    B.plante_doigt(pg, 'rendre le livre', 'Rachel', 0)
    pid = pg.evaluate("()=>{ var p=promises[promises.length-1]; return p.id; }")
    pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600); print('1 ouverte', pg.evaluate(ETAT)); B.capture(pg, 'scratchpad/v145/comm-1-fiche.png')
    r = B.tap_sel(pg, '#dpMsg'); pg.wait_for_timeout(1500); print('2 après toucher « écris un mot »', r, pg.evaluate(ETAT)); B.capture(pg, 'scratchpad/v145/comm-2-touche.png')
    # écrire par le champ de Peaufiner
    pg.evaluate("()=>{ var i=document.getElementById('dCommentInput'); i.value='Merci, je le rends samedi'; var b=document.getElementById('dCommentAdd'); b&&b.click(); }"); pg.wait_for_timeout(1500)
    print('3 commentaire ajouté', pg.evaluate(ETAT)); B.capture(pg, 'scratchpad/v145/comm-3-ajoute.png')
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600); print('4 rouverte', pg.evaluate(ETAT)); B.capture(pg, 'scratchpad/v145/comm-4-rouverte.png')
    # une parole REÇUE, avec un commentaire de l'autre
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); B.plante_doigt(pg, 'venir au concert', 'moi', 0)
    p2 = pg.evaluate("()=>{ var p=promises[promises.length-1]; p.from='Marion'; p.who='moi'; p.comments=[{t:'Promis, j\\u2019y serai',d:new Date(Date.now()-86400000).toISOString(),by:'Marion'}]; return p.id; }")
    pg.evaluate("id=>openDetail(id)", p2); pg.wait_for_timeout(2600); print('5 reçue', pg.evaluate(ETAT)); B.capture(pg, 'scratchpad/v145/comm-5-recue.png')
    pg.evaluate("()=>{ var t=document.getElementById('dpdTog'); t&&t.click(); }"); pg.wait_for_timeout(1800); print('6 Peaufiner', pg.evaluate(ETAT)); B.capture(pg, 'scratchpad/v145/comm-6-peaufiner.png')
    b.close()

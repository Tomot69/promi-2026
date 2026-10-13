import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
GEO = """()=>{ var d=document.getElementById('device').getBoundingClientRect(), k=d.width/390, out={};
  ['dptNat','dptQui','dptTitre','dpTrameCv','tenirZone','tenirCv','dAura','dpPeaufBarre','dptEtat','dptTrace','dpMain'].forEach(function(id){ var e=document.getElementById(id); if(!e) return; var r=e.getBoundingClientRect(); var cs=getComputedStyle(e);
    out[id]={x:Math.round((r.left-d.left)/k),y:Math.round((r.top-d.top)/k),w:Math.round(r.width/k),h:Math.round(r.height/k),t:(e.textContent||'').trim().slice(0,60),fs:cs.fontSize,vis:cs.visibility+'/'+cs.display}; });
  var cv=document.getElementById('dpTrameCv'); out.trait=cv&&cv.getAttribute('data-trait'); out.cls=document.getElementById('detailPoster').className;
  out.textes=[...document.querySelectorAll('#detailPoster *')].filter(function(e){ if(!e.childNodes.length) return false; var t=[...e.childNodes].filter(n=>n.nodeType===3&&n.nodeValue.trim()).map(n=>n.nodeValue.trim()).join(' '); if(!t) return false; var r=e.getBoundingClientRect(); var cs=getComputedStyle(e); return r.width>2&&r.height>2&&cs.visibility!=='hidden'&&cs.display!=='none'&&+cs.opacity>0.1&&r.top>=d.top&&r.bottom<=d.bottom+2; })
     .map(function(e){ var r=e.getBoundingClientRect(); return [(e.id||e.className||e.tagName)+'', [...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.nodeValue.trim()).join(' ').slice(0,44), Math.round((r.left-d.left)/k), Math.round((r.top-d.top)/k), Math.round(r.width/k), Math.round(r.height/k), getComputedStyle(e).fontSize]; });
  return out; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, sombre='sombre' in sys.argv); pg = B.ouvre(ctx)
    B.plante(pg, 'rendre le livre', 'moi', 0); B.plante(pg, 'écrire à Lou', 'Rachel', 0); B.plante(pg, 'le grand plongeoir', 'Marion', 1); B.plante(pg, 'courir dimanche', 'Rachel, Marion, Nico', 1)
    P = pg.evaluate("()=>promises.map(p=>({id:p.id,title:p.title,who:p.who,chiche:!!p.chiche,status:p.status,avec:p.avec,from:p.from,aussi:p.aussi}))"); print(P)
    for i, pr in enumerate(P):
        pg.evaluate("id=>{ closeAll(); openDetail(id); }", pr['id']); pg.wait_for_timeout(2600)
        B.capture(pg, 'scratchpad/v145/fiche-%d%s.png' % (i, '-sombre' if 'sombre' in sys.argv else ''))
        g = pg.evaluate(GEO); print('\n===', pr['title'], '|', pr['who'], '| chiche', pr['chiche'], '| trait', g.get('trait'), '|', g.get('cls'))
        for t in g['textes']: print('   ', t)
    b.close()

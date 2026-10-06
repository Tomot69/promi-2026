import io,ast
S=io.open('app.html',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:60],S.count(a)); S=S.replace(a,b)
r("""#stpDots .stp-dot{width:9px;height:9px;border-radius:50%;background:var(--on-ground,var(--c-creme95));
  opacity:.38;cursor:pointer;flex:none}
#stpDots .stp-dot.on{width:14px;height:14px;opacity:1}""",
"""/* ⚑ v135 (Tom, 6 oct. 2026, C-011) — « Ces points sont interdits par la loi des points (ils ne disent pas qu'il manque quelque chose) :
   s'ils servent de pagination, remplace-les par autre chose. » La pagination des mondes est une rangée de BARRETTES (10 × 4, la courante
   18 × 4) ; toucher une barrette mène toujours à son monde. */
#stpDots .stp-dot{width:10px;height:4px;border-radius:2px;background:var(--on-ground,var(--c-creme95));
  opacity:.38;cursor:pointer;flex:none}
#stpDots .stp-dot.on{width:18px;height:4px;opacity:1}""")
r("var n=src.length, larg=342-2*22, pts=9*Math.max(0,n-1)+14, gap=n>1?Math.min(13,(larg-pts)/(n-1)):0;","var n=src.length, larg=342-2*22, pts=10*Math.max(0,n-1)+18, gap=n>1?Math.min(13,(larg-pts)/(n-1)):0;   /* v135 : des barrettes (10, la courante 18) */")
io.open('app.html','w',encoding='utf-8').write(S)
J=io.open('redteam_palettes.py',encoding='utf-8').read()
a="            ok(tag+' les 24 palettes choisies une à une : le menu reste juste à chaque toucher', not ko, ko[:4])"
assert J.count(a)==1
J=J.replace(a,'''            # ⚑ v135 (Tom, C-011) — « chaque palette doit s'afficher avec ses teintes » : on COMPTE les teintes peintes, sur la capture, pastille par pastille
            if SONDE=='vide': pg.evaluate("()=>{ const s=document.createElement('style'); s.textContent='#stpPals .st3-q{display:none!important}'; document.head.appendChild(s); }")
            import io as _io
            from PIL import Image as _Im
            geo=pg.evaluate("""()=>{ const P=Toile.palettes(); return [...document.querySelectorAll('#stpPals .st3-pals > *')].filter(e=>e.getBoundingClientRect().width>0).map(e=>{ const o=e.querySelector('.st3-orb')||e, r=o.getBoundingClientRect(); return {cle:e.getAttribute('data-p'), x:r.left, y:r.top, w:r.width, h:r.height, cols:(P[e.getAttribute('data-p')]||{cols:[]}).cols.map(c=>c.slice(0,3).map(Math.round))} }) }""")
            im=_Im.open(_io.BytesIO(pg.screenshot())).convert('RGB'); k=im.width/430.0; manque=[]
            for q in geo:
                vues=set()
                for (fx,fy) in ((0.3,0.3),(0.7,0.3),(0.3,0.7),(0.7,0.7)):
                    px=im.getpixel((int((q['x']+q['w']*fx)*k), int((q['y']+q['h']*fy)*k)))
                    for j,c in enumerate(q['cols']):
                        if sum(abs(px[t]-c[t]) for t in range(3))<=18: vues.add(j); break
                att=len(set(tuple(c) for c in q['cols']))
                if q['w']<36 or len(vues)<min(4,att): manque.append('%s : %d teinte(s) sur %d, orbe %.0f pt'%(q['cle'],len(vues),att,q['w']))
            ok(tag+' chaque pastille montre SES teintes à l\\'écran (comptées sur la capture, 24 pastilles × 4)', len(geo)==24 and not manque, manque[:4] or '%d pastilles'%len(geo))
            pts=pg.evaluate("()=>[...document.querySelectorAll('#studioScreen #stpDots > *, #stpPals .st3-dot')].map(e=>{const r=e.getBoundingClientRect(); return [Math.round(r.width*10)/10, Math.round(r.height*10)/10]}).filter(v=>v[0]>0&&v[0]<1.6*v[1])")
            ok(tag+' la pagination des mondes n\\'est pas une rangée de points (loi des points) : des barrettes', not pts, '%d point(s) %s'%(len(pts),pts[:2]))
'''+a)
a="F=[a for a in sys.argv[1:] if not a.startswith('--')]; F=F[0] if F else 'app.html'"; assert J.count(a)==1
J=J.replace(a,a+"\nSONDE=next((x.split('=')[1] for x in sys.argv if x.startswith('--sonde=')), None)   # v135 : --sonde=vide (les teintes des pastilles ne sont plus peintes)")
# v135 : la séquence de Tom — ouvrir le Studio, fermer, rouvrir, PUIS ouvrir le menu — est déjà le tour 2 ; un tour 3 ferme le menu avant de fermer le Studio
J=J.replace("        for tour in (1,2):","        for tour in (1,2,3):   # v135 (C-011) : trois ouvertures — la 3e après avoir fermé le menu par RETOUR avant de fermer le Studio")
ast.parse(J); io.open('redteam_palettes.py','w',encoding='utf-8').write(J)

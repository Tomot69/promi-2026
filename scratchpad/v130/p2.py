import io
S=io.open('redteam_decoupe.py',encoding='utf-8').read()
a="""if __name__ == '__main__':
    sys.exit(main())"""
assert S.count(a)==1
S=S.replace(a,'''# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ⚑ v130 (Tom, C-048 — RÉCIDIVE) — FAMILLE G2 : UNE DALLE SEULE NE PORTE AUCUN MORCEAU DE LA TOILE.
#   « Dans les fiches, l'Index, le Fil et le fil d'un Cercle, on voit de nouveau des morceaux de Toile capturés dans un cadre, au lieu
#   de vraies dalles engendrées, avec leur forme et leur contour réels. […] redteam_decoupe doit couvrir tous ces écrans, Fil d'un
#   Cercle compris, et rougir sur l'état actuel. »
#   POURQUOI LES FAMILLES A–F NE LE VOYAIENT PAS : elles piègent ce que les ÉCRANS font d'une dalle (rogner, redimensionner, relire).
#   Ici la découpe était DANS le moteur : `dalleTrame` peignait la Toile autour de la dalle puis l'effaçait hors de la cellule.
#   CE QUE G2 MESURE : chaque dalle que le moteur rend seule (`Toile.dalleTrame`, piégé) pendant qu'on ouvre la fiche d'un Promi,
#   l'Index, le Fil, la fiche d'un Cercle et son fil défilé, sous les cinq mondes à trame, en clair et en sombre (palette Ingénu :
#   une dalle y a UNE couleur). Dans son canevas, la part des pixels opaques qui ne sont PAS de sa couleur — des éclats des voisines
#   ou du fond de la Toile — doit être nulle : décidé ≤ 0,3 % (l'anticrénelage), EN DUR.
#   Preuve : APP_DECOUPE=…/une copie servie avec le moteur d'avant v130 → ROUGE.
G2_MONDES = ['pixel', 'braille', 'mosaique', 'gravure', 'sillons']
G2_MAX = 0.3
G2_PIEGE = r"""()=>{ if(window.__g2) return; window.__g2=[]; const f=Toile.dalleTrame;
  Toile.dalleTrame=function(dcv,pid,k,monde,opts){ const r=f.apply(this,arguments);
    try{ const g=dcv.getContext('2d'), w=dcv.width, h=dcv.height; if(w&&h){ const d=g.getImageData(0,0,w,h).data, H={}; let n=0;
        for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; n++; const q=(d[i]>>3)+','+(d[i+1]>>3)+','+(d[i+2]>>3); H[q]=(H[q]||0)+1; }
        let m=null,mc=0; for(const q in H) if(H[q]>mc){ mc=H[q]; m=q; }
        if(m&&n>60){ const c=m.split(',').map(v=>v*8+4); let au=0;
          for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; if(Math.max(Math.abs(d[i]-c[0]),Math.abs(d[i+1]-c[1]),Math.abs(d[i+2]-c[2]))>48) au++; }
          window.__g2.push({pid:pid, monde:Toile.getTheme(), n:n, autres:+(100*au/n).toFixed(2), ecran:window.__g2e||''}); } } }catch(e){}
    return r; }; }"""
G2_ECRANS = [('fiche Promi', "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"),
             ('Index', "()=>{closeAll(); setView('toile'); ouvrirIndex();}"),
             ('Fil', "()=>{closeAll(); document.getElementById('filBtn').click();}"),
             ('fiche Cercle et son fil', "()=>{closeAll(); openEssaim('potager');}"),
             ('fil du Cercle, défilé', "()=>{ const l=document.querySelector('#detailPoster .nf-liste, #detailPoster [class*=nf-]'); let n=l; while(n&&n.scrollHeight<=n.clientHeight+4) n=n.parentElement; if(n) n.scrollTop=n.scrollHeight; }")]

def famille_g2():
    from playwright.sync_api import sync_playwright
    ko = 0; total = 0
    print('\\n— FAMILLE G2 (v130) · une dalle seule ne porte aucun morceau de la Toile — ≤ %.1f %% de pixels d\\'une autre couleur —' % G2_MAX)
    with sync_playwright() as p:
        b = p.webkit.launch()
        for th in ('light', 'dark'):
            ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
            pg = ctx.new_page(); pg.goto(APP); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{Toile.setPalette&&Toile.setPalette('signal')}catch(e){}}")
            pg.evaluate(G2_PIEGE)
            for m in G2_MONDES:
                pg.evaluate("(m)=>{closeAll(); Toile.setTheme(m); window.__g2.length=0;}", m); pg.wait_for_timeout(2500)
                vus = {}
                for nom, js in G2_ECRANS:
                    pg.evaluate("(n)=>{window.__g2e=n}", nom); pg.evaluate(js); pg.wait_for_timeout(2600)
                R = pg.evaluate("()=>window.__g2.filter(r=>r.monde===Toile.getTheme())")
                for nom, _ in G2_ECRANS:
                    L = [r for r in R if r['ecran'] == nom]
                    if not L: continue
                    pire = max(r['autres'] for r in L); total += 1; bon = pire <= G2_MAX
                    if not bon: ko += 1
                    print('  %s  %-9s %-5s %-26s %3d dalle(s) rendue(s) · au pire %.2f %% de pixels d\\'une autre couleur' % ('OK' if bon else 'KO', m, th, nom, len(L), pire))
                ecr = set(r['ecran'] for r in R)
                if not R: ko += 1; print('  KO  %-9s %-5s aucune dalle rendue par le moteur : le piège n\\'a rien vu' % (m, th))
            ctx.close()
        b.close()
    print('%s  G2 : %d écran(s) × monde × thème jugés, %d en défaut' % ('✅' if not ko else '❌', total, ko))
    return 1 if ko else 0

if __name__ == '__main__':
    _r1 = 0 if '--g2-seul' in sys.argv else main()
    _r2 = famille_g2()
    sys.exit(1 if (_r1 or _r2) else 0)''')
io.open('redteam_decoupe.py','w',encoding='utf-8').write(S)

import io
S=io.open('redteam_zone.py',encoding='utf-8').read()
a="""        juge('[%s] aucune erreur de page' % th, not er, '; '.join(er[:2]))
        ctx.close()"""
assert S.count(a)==1
S=S.replace(a,"""        # ⚑ v130 (Tom, C-002 — RÉCIDIVE) — C · LE CHEMIN EXACT : Aura, Studio, Studio de nouveau, Aura. « En sombre, la Pelote retrouve son
        #   contour dédoublé derrière elle après la deuxième ouverture du Studio. » La cause : la Pelote perd son contexte graphique (le
        #   Studio en ouvre d'autres ; sur l'iPhone le plus ancien est repris), un canevas neuf est fabriqué, et l'ANCIEN restait affiché
        #   par-dessus, figé sur la Pelote d'avant. Le juge joue le chemin et PROVOQUE cette perte pendant que le Studio est ouvert
        #   (`WEBGL_lose_context`, le même événement), puis compte : UN seul canevas de la carte dans `.au-bo`, et deux canevas en tout.
        def _studio(perte):
            pg.evaluate("()=>{ try{closeAll()}catch(e){} const x=document.querySelector('#auraScreen .closeb'); if(x && document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click(); }"); pg.wait_for_timeout(600)
            pg.evaluate("()=>{ document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2400)
            r = pg.evaluate("()=>{ const c=document.getElementById('auBouleGL'); if(!c) return 'sans'; const g=c.getContext('webgl2'); const e=g&&g.getExtension('WEBGL_lose_context'); if(e){ e.loseContext(); return 'perdu'; } return 'deja'; }") if perte else '-'
            pg.evaluate("()=>{ const x=document.querySelector('#studioScreen .closeb')||document.querySelector('#stcCadre .closeb'); if(x) x.click(); else closeAll(); }"); pg.wait_for_timeout(1200)
            return r
        pg.evaluate("()=>{ try{closeAll()}catch(e){} document.getElementById('souffleBtn').click(); }"); pg.wait_for_timeout(3500)
        gl0 = pg.evaluate("()=>!!document.getElementById('auBouleGL')")
        p1 = _studio(True); _studio(False)
        pg.evaluate("()=>{ try{closeAll()}catch(e){} document.getElementById('souffleBtn').click(); }"); pg.wait_for_timeout(3500)
        cz = pg.evaluate("()=>({gl:document.querySelectorAll('.au-bo canvas#auBouleGL').length, tous:[...document.querySelectorAll('.au-bo canvas')].map(c=>(c.id||'sans nom')).join(' + ')})")
        if gl0:
            juge('C · [%s] Aura, Studio, Studio, Aura : le contexte de la Pelote est bien perdu en chemin' % th, p1 == 'perdu', p1)
            juge('C · [%s] après ce chemin, UN seul canevas de la carte derrière la Pelote, aucun ancien resté dessous' % th, cz['gl'] == 1 and cz['tous'] == 'auBoule + auBouleGL', cz['tous'])
        else:
            print('    (pas de carte graphique à ce banc : le chemin C ne se juge pas)')
        juge('[%s] aucune erreur de page' % th, not er, '; '.join(er[:2]))
        ctx.close()""")
io.open('redteam_zone.py','w',encoding='utf-8').write(S)

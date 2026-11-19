"""v210 (C-302) — la rotation de la Pelote : 5 minutes simulées par la loi de l'app (`_peloteDerive.simule`, trois graines), puis 20 s de la vraie Pelote
(l'Aura ouverte, chaque image). D'une image à l'autre (1/60 s) : l'axe tourne de moins de 0,5°, la vitesse change de moins de 0,5 % ; en 1 s, la direction
du mouvement tourne de moins de 30° (aucune inversion) ; la vitesse moyenne est celle de C-298 (un tour en 66,7 s) à 5 % ; l'inclinaison ne colle jamais
à sa borne. `--sonde` : une inversion d'axe posée au milieu de la série — il rougit."""
import sys, math; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html'); SONDE = '--sonde' in sys.argv
AUTO = 2 * math.pi / (100 / 1.5); TANGMAX = 1.15
ok = tot = 0
def juge(c, m, d=''):
    global ok, tot
    tot += 1; ok += bool(c); print(('  ✅ ' if c else '  ❌ ') + m + ('   ' + d if d else ''))
def ang(a, b):
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(x * x for x in b))
    if na < 1e-12 or nb < 1e-12: return 0
    return math.degrees(math.acos(max(-1, min(1, sum(x * y for x, y in zip(a, b)) / na / nb))))
def serie(L, dt, nom):
    W = [l[:3] for l in L]; n = len(W)
    if SONDE: W = W[:n // 2] + [[-x for x in w] for w in W[n // 2:]]
    pas = max(ang(W[i], W[i + 1]) for i in range(n - 1))
    vit = [math.sqrt(sum(x * x for x in w)) for w in W]
    dv = max(abs(vit[i + 1] - vit[i]) / max(vit[i], 1e-9) for i in range(n - 1))
    s1 = int(round(1 / dt)); sec = max(ang(W[i], W[i + s1]) for i in range(0, n - s1, max(1, s1 // 6)))
    moy = sum(vit) / n
    juge(pas < 0.5, '%s : l\'axe tourne de moins de 0,5° d\'une image à l\'autre' % nom, 'au plus %.3f°' % pas)
    juge(dv < 0.005, '%s : la vitesse change de moins de 0,5 %% d\'une image à l\'autre' % nom, 'au plus %.3f %%' % (dv * 100))
    juge(sec < 30, '%s : en 1 s, la direction tourne de moins de 30° (aucune inversion)' % nom, 'au plus %.1f°' % sec)
    return moy
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
    for g in (12345, 777, 4242):
        L = pg.evaluate('(g)=>window._peloteDerive.simule(300, 1/60, g)', g)
        moy = serie(L, 1 / 60, 'simulé, graine %d' % g)
        juge(abs(moy / AUTO - 1) < 0.05, 'simulé, graine %d : la vitesse moyenne est celle de C-298 à 5 %%' % g, '%.4f rad/s pour %.4f' % (moy, AUTO))
        tmax = max(abs(l[3]) for l in L); juge(tmax < TANGMAX - 0.01, 'simulé, graine %d : l\'inclinaison ne colle jamais à sa borne' % g, '|tan| au plus %.3f (borne %.2f)' % (tmax, TANGMAX))
        segs = []; # la durée des dérives varie : les changements de cible (l'axe repart d'une vitesse nulle)
    # la vraie Pelote : 20 s, chaque image — la vitesse vue (lac, tan, tour à plat)
    pg.evaluate("()=>{ try{closeAll();}catch(e){} document.getElementById('souffleBtn').click(); }"); pg.wait_for_timeout(4000)
    R = pg.evaluate("""()=>new Promise(r=>{ const L=[]; const t0=performance.now(); let av=null; (function f(){ const e=window._aura.etat(), ro=window._peloteRotation().angle*Math.PI/180, t=performance.now();
        if(av){ const dt=(t-av[0])/1000; if(dt>0.004) L.push([(e.tan-av[2])/dt, (e.lac-av[1])/dt, (ro-av[3])/dt, dt]); } av=[t, e.lac, e.tan, ro];
        if(t-t0<20000) requestAnimationFrame(f); else r(L); })(); })""")
    dts = sorted(r[3] for r in R); med = dts[len(dts) // 2]
    R2 = [r for r in R if r[3] < 2.2 * med]   # une image longue (le banc) n'est pas une saccade de la loi
    juge(len(R2) > 200, 'la vraie Pelote : la vue bouge à chaque image (la rotation est rendue)', '%d images, %d gardées' % (len(R), len(R2)))
    if len(R2) > 50:
        W = [r[:3] for r in R2]; pas = sorted(ang(W[i], W[i + 1]) for i in range(len(W) - 1))
        juge(pas[int(len(pas) * 0.99)] < 2, 'la vraie Pelote : la direction du mouvement ne saute pas d\'une image à l\'autre', 'p99 %.2f°, au plus %.2f° (le pas d\'horloge des images compte)' % (pas[int(len(pas) * 0.99)], pas[-1]))
        vit = [math.sqrt(sum(x * x for x in w)) for w in W]; moy = sum(vit) / len(vit)
        juge(abs(moy / AUTO - 1) < 0.2, 'la vraie Pelote : sa vitesse est celle de C-298 (à 20 %, 20 s seulement)', '%.4f rad/s pour %.4f' % (moy, AUTO))
    b.close()
print('\n  %s  %d / %d' % ('✅' if ok == tot else '❌', ok, tot))

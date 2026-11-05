#!/usr/bin/env python3
"""redteam_ecran_allume.py — ⚑ v180a (Tom, C-236) : « tant que Promi est au premier plan, l'écran reste allumé, même posé sans être touché ».

Banc WebKit sur l'état exporté de Tom (veille rétablie) :
  W · Wake Lock présent (simulé, la demande réussit) : après un toucher, Wake Lock est demandé, AUCUNE vidéo n'est créée.
  V · Wake Lock absent (le cas de l'iPhone en http) : rien avant le premier toucher ; au premier toucher une vidéo est lancée — hors de l'écran,
      sans contrôles, sans `loop` (WebKit ne retient pas l'écran pour une vidéo en boucle) ; elle joue encore 70 s plus tard, sans un toucher,
      la veille partie entre-temps ; son temps avance (elle ne s'arrête jamais à sa fin).
  R · après le délai de relâchement de la veille (abaissé pour le juge), la vidéo s'arrête ; un toucher la relance.
  H · la page cachée : la vidéo s'arrête ; rendue visible, un toucher la relance.
  S · la piste son de la vidéo est un silence (décodée hors du navigateur, `afconvert` : tous les échantillons à 0).
Rouge sur v179b (`--fichier=zz-v179b.html`) : aucune vidéo.
"""
import sys, re, io, base64, os, subprocess, tempfile, time; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
SANS = "Object.defineProperty(Navigator.prototype,'wakeLock',{get:function(){return undefined;},configurable:true});"
AVEC = """(function(){ var n=0; window.__wl=function(){return n;}; var W={request:function(){ n++; return Promise.resolve({release:function(){return Promise.resolve();}, addEventListener:function(){}}); }};
  Object.defineProperty(Navigator.prototype,'wakeLock',{get:function(){return W;},configurable:true}); })();"""
ETAT = """()=>{ var v=document.getElementById('promiEveil'), e=window._veille&&window._veille(); var r=v?v.getBoundingClientRect():null;
  return {existe:!!v, joue:v?!v.paused:false, fin:v?v.ended:null, temps:v?v.currentTime:null, loop:v?v.loop:null, ctrl:v?v.controls:null,
    hors:r?(r.right<=0||r.bottom<=0||r.left>=innerWidth||r.top>=innerHeight):null, eveil:e?e.eveil:null, veille:e?e.active:null}; }"""
def silence():
    S = io.open(F, encoding='utf-8').read(); m = re.search(r"EVEIL_SRC='data:video/mp4;base64,([A-Za-z0-9+/=]+)'", S)
    if not m: return None, 'pas de vidéo dans la page'
    d = tempfile.mkdtemp(); mp4 = os.path.join(d, 'e.mp4'); wav = os.path.join(d, 'e.wav')
    open(mp4, 'wb').write(base64.b64decode(m.group(1)))
    subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16', mp4, wav], check=True, capture_output=True)
    w = open(wav, 'rb').read(); i = w.find(b'data'); pcm = w[i + 8:]
    mx = max((abs(int.from_bytes(pcm[k:k + 2], 'little', signed=True)) for k in range(0, len(pcm) - 1, 2)), default=0)
    return mx == 0, '%d échantillons, max |x| = %d' % (len(pcm) // 2, mx)
def page(b, init):
    ctx, d = B.contexte_tom(b)
    if not ctx: print('pas d\'état exporté'); sys.exit(2)
    ctx.add_init_script(init)
    pg = B.ouvre(ctx, F, 300); pg.evaluate("()=>localStorage.removeItem('promi_veille_off')")
    pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6500); return ctx, pg, d
with sync_playwright() as p:
    b = p.webkit.launch()
    # W
    ctx, pg, d = page(b, AVEC); print('  état :', d['_fichier'], '·', F)
    B.tap(pg, 200, 400); pg.wait_for_timeout(600)
    e = pg.evaluate(ETAT)
    juge('W · Wake Lock présent : demandé au toucher, aucune vidéo créée', pg.evaluate("()=>window.__wl()") >= 1 and not e['existe'], e)
    ctx.close()
    # V
    ctx, pg, d = page(b, SANS)
    e0 = pg.evaluate(ETAT)
    B.tap(pg, 200, 400); pg.wait_for_timeout(900)
    e1 = pg.evaluate(ETAT)
    juge('V · Wake Lock absent : rien avant le premier toucher', not e0['existe'], e0)
    juge('V · au premier toucher, la vidéo joue (hors de l\'écran, sans contrôles, sans `loop`)', e1['existe'] and e1['joue'] and e1['hors'] and e1['loop'] is False and e1['ctrl'] is False, e1)
    temps = []; t0 = time.time(); fin = False; arret = False; veille = False
    while time.time() - t0 < 70:
        pg.wait_for_timeout(2000); e = pg.evaluate(ETAT); temps.append(round(e['temps'] or 0, 2))
        fin = fin or bool(e['fin']); arret = arret or not e['joue']; veille = veille or bool(e['veille'])
    juge('V · 70 s sans un toucher : la vidéo joue toujours, la veille est partie, jamais arrêtée à sa fin', not arret and not fin and veille and len(set(temps)) > 10, 'temps %s… · veille %s' % (temps[:8], veille))
    # R
    pg.evaluate("()=>{ window._veilleRegle.VERROU=2000; }"); pg.wait_for_timeout(3500)
    e = pg.evaluate(ETAT)
    juge('R · relâché après le délai de la veille : la vidéo s\'arrête', e['veille'] and not e['joue'] and e['eveil']['etat'] == 'relâché', e)
    B.tap(pg, 200, 400); pg.wait_for_timeout(900); e = pg.evaluate(ETAT)
    juge('R · un toucher quitte la veille et relance la vidéo', (not e['veille']) and e['joue'], e)
    # H
    pg.evaluate("""()=>{ Object.defineProperty(document,'visibilityState',{get:()=>'hidden',configurable:true}); Object.defineProperty(document,'hidden',{get:()=>true,configurable:true});
      document.dispatchEvent(new Event('visibilitychange')); }"""); pg.wait_for_timeout(400); e = pg.evaluate(ETAT)
    juge('H · la page cachée : la vidéo s\'arrête', not e['joue'], e)
    pg.evaluate("""()=>{ Object.defineProperty(document,'visibilityState',{get:()=>'visible',configurable:true}); Object.defineProperty(document,'hidden',{get:()=>false,configurable:true});
      document.dispatchEvent(new Event('visibilitychange')); }"""); pg.wait_for_timeout(300)
    B.tap(pg, 200, 400); pg.wait_for_timeout(900); e = pg.evaluate(ETAT)
    juge('H · rendue visible, un toucher la relance', e['joue'], e)
    ctx.close(); b.close()
ok, dd = silence(); juge('S · la piste son est un silence', ok, dd)
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)

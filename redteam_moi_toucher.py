"""⚑ v210 (Tom, 18 nov. 2026, C-304) — « Quand on touche la place du destinataire (« à qui ose ? », « à qui ? », « avec qui ? »), le menu des membres se déroule
avec « moi » déjà coché, mais la phrase dit encore « qui ». Dès qu'on touche, PENDANT que le menu se déroule, la phrase passe à « moi », par détracé puis tracé ;
quitté sans rien changer, elle reste « à moi » ; elle reflète toujours ce qui est coché dès qu'il a été ouvert. Trois natures. »
Sur chaque nature, au doigt : A avant, le mot d'attente ; B toucher la place → « moi » (en pointillés) tracé PENDANT que le menu se déroule (le tracé part dans les
900 ms), l'attente détracée d'abord, « Moi » coché ; C fermer sans rien changer → « moi » ; D ajouter Rachel → « Rachel » tracé ; E retirer Rachel → « moi » tracé ;
F retirer « Moi » seul → « moi » reste. Échelles 1 et 0,79. `--fichier=zz-v209.html` : rouge (B)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
NATS = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--natures=')), 'promi,chiche,nuee').split(',')
ATT = {'promi': 'qui ?', 'chiche': 'qui ose ?', 'nuee': 'tout le monde'}
ok = tot = 0
def juge(m, c, d=''):
    global ok, tot
    tot += 1; ok += bool(c); print('  %s %s %s' % ('✅' if c else '❌', m, '' if c else str(d)[:240]), flush=True)
SUIT = """()=>{ window.__mt=[]; const T=window.TraceLettres; if(T && !T.__m2){ T.__m2=1; const t=T.trace; T.trace=function(c,x,o){ const sel='#csPhrase .ph-m[data-ph="qui"], #nueePhrase .ph-m[data-np="avec"]';
  const pl=c && c.matches && (c.matches(sel) || (c.matches('.v200-mt') && c.parentElement && c.parentElement.matches(sel)));
  if(pl && !(o&&o.preparer)) window.__mt.push([(o&&o.inverse)?'detrace':'trace', (c.textContent||'').replace(/\\s+/g,' ').trim(), Math.round(performance.now())]); return t.apply(this, arguments); }; } }"""
ST = """k=>{ const e=document.querySelector(k==='nuee'?'#nueePhrase .ph-m[data-np="avec"]':'#csPhrase .ph-m[data-ph="qui"]'); const m=document.querySelector('#createSheet .gn [data-gn-tete]');
  return {txt:e&&(e.textContent||'').replace(/\\s+/g,' ').replace(/,\\s*$/,'').trim(), vide:!!(e&&e.classList.contains('ph-vide')), moi:m?m.classList.contains('on'):null, t:Math.round(performance.now())}; }"""
def mt(pg): r = pg.evaluate("()=>{ const r=window.__mt||[]; window.__mt=[]; return r; }"); return r
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_moi_toucher — %s · charge %.1f' % (F, B.charge()))
    for vw, vh, ech in ((430, 932, '1'), (330, 714, '0,79')):
        for k in NATS:
            T = '[%s ×%s]' % (k, ech); sel = '#nueePhrase .ph-m[data-np="avec"]' if k == 'nuee' else '#csPhrase .ph-m[data-ph="qui"]'
            ctx = B.contexte(b, vw=vw, vh=vh); pg = B.ouvre(ctx, F)
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % k); pg.wait_for_timeout(2600)
            if k == 'promi': B.tap_sel(pg, '#csPhrase .ph-b[data-ph="sens"]'); pg.wait_for_timeout(2400)
            pg.evaluate(SUIT); e = pg.evaluate(ST, k)
            juge(T + ' A · avant : « %s »' % ATT[k], e['txt'] == ATT[k] and e['vide'], e)
            t0 = pg.evaluate("()=>Math.round(performance.now())"); mt(pg); B.tap_sel(pg, sel); pg.wait_for_timeout(1600); e = pg.evaluate(ST, k); m = mt(pg)
            tr = [x for x in m if x[0] == 'trace' and x[1] == 'moi']; de = [x for x in m if x[0] == 'detrace']
            juge(T + ' B · toucher la place : « moi » en pointillés, « Moi » coché', e['txt'] == 'moi' and e['vide'] and e['moi'], e)
            juge(T + ' B · l\'attente détracée puis « moi » tracé, pendant que le menu se déroule (≤ 900 ms)', de and tr and tr[0][2] - t0 <= 900 and de[0][2] <= tr[0][2], m)
            B.tap(pg, 195, 200); pg.wait_for_timeout(2600); e = pg.evaluate(ST, k); mt(pg)
            juge(T + ' C · fermé sans rien changer : « moi » reste', e['txt'] == 'moi' and e['vide'], e)
            B.tap_sel(pg, sel); pg.wait_for_timeout(1300); B.tap_sel(pg, '#createSheet .gn > .ph-add'); pg.wait_for_timeout(400); pg.keyboard.type('Rachel', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(1400)
            B.tap(pg, 195, 200); pg.wait_for_timeout(2800); e = pg.evaluate(ST, k); m = mt(pg)
            juge(T + ' D · Rachel ajoutée : « Rachel », tracé', e['txt'] == 'Rachel' and not e['vide'] and any(x[0] == 'trace' and 'Rachel' in x[1] for x in m), [e, m])
            B.tap_sel(pg, sel); pg.wait_for_timeout(1300); B.tap_sel(pg, '#createSheet .gn .gn-liste .ph-o.on[data-v="Rachel"] .ppo-x'); pg.wait_for_timeout(900); B.tap(pg, 195, 200); pg.wait_for_timeout(2800)
            e = pg.evaluate(ST, k); m = mt(pg)
            juge(T + ' E · Rachel retirée : « moi », tracé', e['txt'] == 'moi' and e['vide'] and any(x[0] == 'trace' and x[1] == 'moi' for x in m), [e, m])
            B.tap_sel(pg, sel); pg.wait_for_timeout(1300); B.tap_sel(pg, '#createSheet .gn [data-gn-tete] .ppo-x'); pg.wait_for_timeout(900); e = pg.evaluate(ST, k)
            B.tap(pg, 195, 200); pg.wait_for_timeout(2400); e2 = pg.evaluate(ST, k)
            juge(T + ' F · « Moi » retiré seul : « moi » reste', e['txt'] == 'moi' and e2['txt'] == 'moi' and e2['vide'], [e, e2])
            ctx.close()
    b.close()
print('\nredteam_moi_toucher : %d/%d' % (ok, tot)); sys.exit(0 if ok == tot else 1)

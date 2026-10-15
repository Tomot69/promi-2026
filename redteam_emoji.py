#!/usr/bin/env python3
"""
redteam_emoji.py — PAS D'EMOJI DANS PROMI (v146, Tom, 14 oct. 2026 — C-129).
« Un emoji tapé ou collé n'est tout simplement pas inséré : rien ne s'affiche, aucun message, rien n'est noté. » Partout où l'on écrit : la phrase de la
page + (le titre), le prénom de l'onboarding, une personne ajoutée, un commentaire, la note de Peaufiner. Banc WebKit, au clavier (Playwright tape chaque
caractère : un emoji arrive comme une insertion de texte), au collage (un vrai évènement `paste` avec son presse-papiers), en mélange ; puis la sauvegarde.
EN DUR : pictogrammes, teintes de peau, jonctions (famille), drapeaux, touches numérotées. Le texte autour reste, à l'espace près.
Preuve (§7) : `--fichier=zz-avant-v146.html` — il rougit (les emojis entrent).
"""
import sys, json; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
EMO = ['🏃', '👍🏽', '👨‍👩‍👧', '🇫🇷', '1️⃣', '❤️', '✨']
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('  %s %-110s %s' % ('✅' if c else '❌', nom, str(d)[:230]), flush=True)
VAL = "(s)=>{ const e=document.querySelector(s); if(!e) return null; return e.isContentEditable?e.textContent:e.value; }"
COLLE = """([s, txt])=>{ const e=document.querySelector(s); if(!e) return 'absent'; e.focus(); let dt=null; try{ dt=new DataTransfer(); dt.setData('text/plain', txt); }catch(x){}
  let ev; try{ ev=new ClipboardEvent('paste', {clipboardData:dt, bubbles:true, cancelable:true}); }catch(x){ ev=new Event('paste', {bubbles:true, cancelable:true}); Object.defineProperty(ev, 'clipboardData', {value:{getData:()=>txt}}); }
  if(!ev.clipboardData) Object.defineProperty(ev, 'clipboardData', {value:{getData:()=>txt}});
  const pris=!e.dispatchEvent(ev); if(!pris){ if(typeof e.setRangeText==='function'){ e.setRangeText(txt, e.selectionStart, e.selectionEnd, 'end'); e.dispatchEvent(new Event('input',{bubbles:true})); } }
  return e.isContentEditable?e.textContent:e.value; }"""
MSG = "()=>[...document.querySelectorAll('.toast, .v16-toast, [role=alert], [role=status]')].filter(e=>e.getBoundingClientRect().width>0 && /emoji|caract/i.test(e.textContent)).length"
def essai(pg, sel, nom):
    pg.evaluate("(s)=>{ const e=document.querySelector(s); if(e){ e.focus(); if(e.isContentEditable) e.textContent=''; else e.value=''; } }", sel)
    # le clavier emoji d'iOS insère une séquence ENTIÈRE (une touche numérotée, une teinte de peau) : le texte est tapé, chaque emoji est inséré d'un bloc
    for morceau, emoji in (('marcher ', False), (EMO[0], True), (' une ', False), (EMO[1], True), (' heure ', False), (EMO[4], True)):
        (pg.keyboard.insert_text(morceau) if emoji else pg.keyboard.type(morceau, delay=20))
    pg.wait_for_timeout(200); v1 = pg.evaluate(VAL, sel)
    ok1 = v1 is not None and all(x not in (v1 or '') for x in ''.join(EMO)) and 'marcher' in v1 and 'une' in v1 and 'heure' in v1
    juge('%s · au clavier : le texte reste, les emojis n\'entrent pas' % nom, ok1, repr(v1))
    pg.evaluate("(s)=>{ const e=document.querySelector(s); if(e){ e.focus(); if(e.isContentEditable) e.textContent=''; else e.value=''; } }", sel)
    v2 = pg.evaluate(COLLE, [sel, 'lire %s Proust %s ce %s soir %s' % (EMO[2], EMO[3], EMO[5], EMO[6])]); pg.wait_for_timeout(150); v2 = pg.evaluate(VAL, sel)
    juge('%s · au collage : le texte reste, les emojis (famille, drapeau, cœur, étincelles) n\'entrent pas' % nom, v2 is not None and all(ord(c) < 0x2000 or c in '’…' for c in v2) and 'Proust' in v2 and 'soir' in v2, repr(v2))
    juge('%s · aucun message' % nom, pg.evaluate(MSG) == 0)
with sync_playwright() as p:
    b = p.webkit.launch()
    # 1 · le prénom de l'onboarding (stockage vierge)
    ctx = contexte(b, onb=False, guide=False); pg = ouvre(ctx, F); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ const c=document.getElementById('onbPh'); if(c) c.click(); }"); pg.wait_for_timeout(300)
    essai(pg, '#onbIn', 'le prénom de l\'onboarding'); ctx.close()
    # 2 · la page +, la personne ajoutée, le commentaire, la note ; puis la sauvegarde
    ctx = contexte(b); pg = ouvre(ctx, F)
    pg.evaluate("()=>{ closeAll(); document.getElementById('createBtn').click(); var n=0; (function e(){ var x=[...document.querySelectorAll('#createSheet .tile')][0]; var cs=document.getElementById('createSheet'); if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(e,350); })(); }"); pg.wait_for_timeout(2600)
    tap_sel(pg, '#csPhrase [data-ph=titre]'); pg.wait_for_timeout(500); essai(pg, '#phIn', 'la page + (le titre de la phrase)')
    tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(400)
    plante(pg, 'arroser le ficus', qui='Rachel'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ closeAll(); const q=promises[promises.length-1]; q.from='Rachel'; openDetail(q.id); }"); pg.wait_for_timeout(2600)
    tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(600); essai(pg, '#cm5Ligne .cm5-saisie', 'un commentaire')
    pg.evaluate("()=>{ const s=document.querySelector('#cm5Ligne .cm5-saisie'); s.value=''; s.focus(); }"); pg.keyboard.type('Bravo %s à toi %s' % (EMO[1], EMO[3]), delay=20); pg.keyboard.press('Enter'); pg.wait_for_timeout(600)
    pg.evaluate("()=>{ const q=promises[promises.length-1]; q.title=q.title+' 🌱'; USER.name='Tom 😀'; saveState(); }"); pg.wait_for_timeout(500)
    st = pg.evaluate("()=>localStorage.getItem('promi_state')||localStorage.getItem('promi')||Object.keys(localStorage).filter(k=>/state|promi_v/.test(k)).map(k=>localStorage.getItem(k)).join('')")
    emo_st = [x for x in EMO + ['🌱', '😀'] if x in (st or '')]
    juge('à l\'enregistrement : aucun emoji dans la sauvegarde (le titre, le nom, le commentaire envoyé)', bool(st) and not emo_st and 'Bravo' in st, 'trouvés %s · taille %d' % (emo_st, len(st or '')))
    juge('aucune erreur de page', not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2]); ctx.close(); b.close()
print('\n  %s  %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res))); sys.exit(0 if all(res) else 1)

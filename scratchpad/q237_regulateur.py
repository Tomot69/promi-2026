# -*- coding: utf-8 -*-
"""Q237 — LE RÉGULATEUR DESCEND-IL, ET REMONTE-T-IL ? Mesuré sous bridage CDP.
   ⚠ L'instrument ne doit pas ralentir avec la machine (§7) : on ne cadence rien nous-mêmes,
   on LIT ce que l'app publie (`_aura.etat()`), et le bridage vient du CDP, pas de la page."""
import sys, time, json
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
ETAT = "()=>{try{var e=window._aura.etat();return {palier:e.palier, vise:e.vise, ms:e.ms};}catch(x){return {err:String(x)};}}"
def ouvre(pg):
    pg.evaluate("()=>{try{closeAll();}catch(e){}}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{document.getElementById('souffleBtn').click();}")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
    pg.goto(URL); pg.wait_for_timeout(6200)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{try{localStorage.removeItem('promi_orbite_palier');}catch(e){}}")
    ouvre(pg); pg.wait_for_timeout(5000)
    print('1 · au repos, machine libre     :', pg.evaluate(ETAT))
    print('   -- on bride le CPU ×8 --')
    cdp.send('Emulation.setCPUThrottlingRate',{'rate':8})
    pg.wait_for_timeout(14000)
    print('2 · sous bridage ×8             :', pg.evaluate(ETAT))
    ouvre(pg); pg.wait_for_timeout(9000)
    print('3 · rouvert, toujours bridé     :', pg.evaluate(ETAT))
    print('   -- on relâche le bridage --')
    cdp.send('Emulation.setCPUThrottlingRate',{'rate':1})
    pg.wait_for_timeout(16000)
    print('4 · charge retombée, sans rouvrir:', pg.evaluate(ETAT))
    ouvre(pg); pg.wait_for_timeout(12000)
    print('5 · rouvert, machine libre      :', pg.evaluate(ETAT))
    ouvre(pg); pg.wait_for_timeout(12000)
    print('6 · rouvert encore              :', pg.evaluate(ETAT))
    print('   persisté :', pg.evaluate("()=>localStorage.getItem('promi_orbite_palier')"))
    b.close()

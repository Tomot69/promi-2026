#!/usr/bin/env python3
"""v145 (C-088) — Ritournelle à 1, 2, 3, 4 paroles : captures banc_tom (WebKit 390 × 844 @3x, Toile vide, plantées par l'app), sur une base donnée.
usage : rit.py <port> <fichier> <nom> [sombre]"""
import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
port, fichier, nom = sys.argv[1], sys.argv[2], sys.argv[3]; sombre = 'sombre' in sys.argv
GRAINE = "(function(){ var a=20261013; Math.random=function(){ a|=0; a=a+0x6D2B79F5|0; var t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; })();"
T = ['rendre le livre', 'écrire à Lou', 'arroser le ficus', 'courir dimanche']
out = {}
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, sombre=sombre); ctx.add_init_script(GRAINE)
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:%s/%s' % (port, fichier)); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{ Toile.setTheme('ritournelle'); }catch(e){} }"); pg.wait_for_timeout(1500)
    for i, t in enumerate(T):
        B.plante(pg, t); pg.wait_for_timeout(3000)
        B.capture(pg, 'scratchpad/v145/rit-%s-%d.png' % (nom, i + 1))
        out[i + 1] = pg.evaluate("()=>{ var v=Toile.vue(); var g=[]; try{ g=(window.Toile_graines?Toile_graines():[]).map(function(s){return [Math.round(s.x*10)/10,Math.round(s.y*10)/10,s.kind,s.pid==null?null:1]}); }catch(e){} return {vue:[+v.s.toFixed(3),+v.ox.toFixed(1),+v.oy.toFixed(1)], n:g.length, graines:g, neuf:(Toile.semisNeuf?Toile.semisNeuf():null)}; }")
        print(nom, i + 1, json.dumps(out[i + 1])[:400], flush=True)
    b.close()
io.open('scratchpad/v145/rit-%s.json' % nom, 'w').write(json.dumps(out))

# -*- coding: utf-8 -*-
"""MESURE 1 — la barre du bas : 5 entrées, libellés 12 px, Gilbert Bold capitales contre l'actuel ApfelMid.
   MESURE 2 — le plancher de taille : 13 px en Atkinson contre 13 px en Apfel/ApfelMid (§6, rien sous 12 px)."""
from playwright.sync_api import sync_playwright
import json

MOTS = ["Studio","Aura","Index","Fil"]          # les quatre libellés de la barre (le + n'en a pas)
CENTRES = [70,124,266,320]                       # cotes d'écran, lot-ACCUEIL

def mesure(pg, txt, fam, poids, taille, ls, maj):
    return pg.evaluate("""([txt,fam,poids,taille,ls,maj])=>{
      const s=document.createElement('span'); s.className='m';
      s.style.fontFamily=fam; s.style.fontWeight=poids; s.style.fontSize=taille+'px';
      s.style.letterSpacing=ls; s.style.textTransform=maj?'uppercase':'none';
      s.textContent=txt; document.body.appendChild(s);
      const r=s.getBoundingClientRect(); const w=r.width, h=r.height;
      // hauteur d'x réelle : on peint et on compte
      document.body.removeChild(s);
      return {w:Math.round(w*100)/100,h:Math.round(h*100)/100};
    }""",[txt,fam,poids,taille,ls,maj])

def xheight(pg, fam, poids, taille):
    """hauteur d'x RENDUE, en pixels d'écran (dpr 2), mesurée sur le dessin"""
    return pg.evaluate("""([fam,poids,taille])=>{
      const c=document.createElement('canvas'); c.width=400;c.height=200; const g=c.getContext('2d');
      g.fillStyle='#fff';g.fillRect(0,0,400,200);
      g.fillStyle='#000'; g.font=poids+' '+taille+'px '+fam; g.textBaseline='alphabetic';
      g.fillText('xnome',10,150);
      const d=g.getImageData(0,0,400,200).data; let top=-1,bot=-1;
      for(let y=0;y<200;y++){ let on=false; for(let x=0;x<400;x++){ if(d[(y*400+x)*4]<128){on=true;break;} }
        if(on){ if(top<0) top=y; bot=y; } }
      // largeur d'un H et d'un n pour la chasse
      const wH=g.measureText('H').width, wn=g.measureText('n').width;
      return {x:bot-top+1, wH:Math.round(wH*100)/100, wn:Math.round(wn*100)/100};
    }""",[fam,poids,taille])

with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    pg.goto("http://127.0.0.1:8752/scratchpad/banc_polices.html")
    pg.evaluate("""async()=>{
      const F=[['Gilbert',700],['Atkinson',400],['Atkinson',500],['Atkinson',700],['ApfelMid',500],['Apfel',400],['Bricolage',700],['Bricolage',600]];
      await Promise.all(F.map(([f,w])=>document.fonts.load(w+' 16px '+f)));
      await document.fonts.ready;
    }""")
    pg.wait_for_timeout(1500)
    charge = pg.evaluate("()=>[...document.fonts].map(f=>f.family+'/'+f.weight+'/'+f.status)")
    print("faces :", charge)
    print()
    print("=== MESURE 1 · LA BARRE DU BAS — libellés 12 px, capitales, letter-spacing .08em ===")
    print("    espace entre deux centres voisins : 54 px (centres 70 · 124 | 266 · 320)")
    print(f"    {'mot':8} {'ApfelMid 500 (actuel)':>22} {'Gilbert 700 (proposé)':>22} {'écart':>8}")
    pire=0; pireg=None
    for m in MOTS:
        a=mesure(pg,m,'ApfelMid',500,12,'.08em',True)
        g=mesure(pg,m,'Gilbert',700,12,'.08em',True)
        d=g['w']-a['w']
        if g['w']>pire: pire=g['w']; pireg=m
        print(f"    {m:8} {a['w']:>22.2f} {g['w']:>22.2f} {d:>+8.2f}")
    print(f"    le plus large en Gilbert : {pireg} = {pire:.2f} px")
    # air entre deux libellés voisins : centre à centre 54 − (demi + demi)
    for i in range(len(MOTS)-1):
        if CENTRES[i+1]-CENTRES[i] > 60: continue   # le + est entre 124 et 266
        a1=mesure(pg,MOTS[i],'Gilbert',700,12,'.08em',True); a2=mesure(pg,MOTS[i+1],'Gilbert',700,12,'.08em',True)
        air=(CENTRES[i+1]-CENTRES[i]) - a1['w']/2 - a2['w']/2
        b1=mesure(pg,MOTS[i],'ApfelMid',500,12,'.08em',True); b2=mesure(pg,MOTS[i+1],'ApfelMid',500,12,'.08em',True)
        airA=(CENTRES[i+1]-CENTRES[i]) - b1['w']/2 - b2['w']/2
        print(f"    air {MOTS[i]}↔{MOTS[i+1]} : Gilbert {air:+.2f} px · actuel {airA:+.2f} px")
    print()
    print("=== MESURE 2 · LE PLANCHER — 13 px, hauteur d'x rendue et chasse ===")
    for fam,poids,lib in [('Apfel',400,'Apfel 400 (actuel)'),('ApfelMid',500,'ApfelMid 500 (actuel)'),('Atkinson',400,'Atkinson 400'),('Atkinson',500,'Atkinson 500'),('Atkinson',700,'Atkinson 700')]:
        for t in (12,13,14,16):
            r=xheight(pg,fam,poids,t)
            print(f"    {lib:22} {t} px : hauteur d'x = {r['x']} px · H = {r['wH']} · n = {r['wn']}")
    print()
    print("=== la métadonnée à 13 px / 65 % — la phrase réelle ===")
    for fam,poids,lib in [('ApfelMid',500,'ApfelMid 500'),('Atkinson',400,'Atkinson 400')]:
        r=mesure(pg,'tenu · il y a 2 jours · Quentin',fam,poids,13,'.02em',False)
        print(f"    {lib:14} : largeur {r['w']} px · hauteur de boîte {r['h']} px")
    print()
    print("=== hauteur de ligne NORMALE (le piège des cotes dérivées) ===")
    for fam,poids,lib in [('Apfel',400,'Apfel 400'),('ApfelMid',500,'ApfelMid 500'),('Atkinson',400,'Atkinson 400'),('Bricolage',700,'Bricolage 700'),('Gilbert',700,'Gilbert 700')]:
        r=mesure(pg,'Promi',fam,poids,16,'normal',False)
        print(f"    {lib:16} 16 px → boîte {r['h']} px  (= {r['h']/16:.3f} em)")
    b.close()

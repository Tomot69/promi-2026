#!/usr/bin/env python3
"""LA PREUVE EN PIXELS — on filme, on mesure LES IMAGES, jamais le code.

⚠ DEUX PIÈGES D'INSTRUMENT PAYÉS ICI, ET ILS M'ONT FAIT CONCLURE FAUX UNE FOIS :
  1 · une capture prend 100 à 300 ms. Photographier « pendant » une rotation lancée,
      c'est photographier APRÈS : l'élan s'est amorti, le déplacement est nul, et
      l'image ne montre aucune traînée alors que le code en dessine soixante-sept
      mille. On ENTRETIENT la vitesse pendant toute la capture.
  2 · la fenêtre de mesure est fixe à l'écran. Si la sphère tourne, on compare deux
      scènes différentes. On ARRÊTE la rotation de repos pour les séquences du creux.
"""
from playwright.sync_api import sync_playwright
DOSS='scratchpad/preuve'

with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':430,'height':1000}, device_scale_factor=2)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:8752/PLANCHE-AURA-SPHERE.html')
    pg.wait_for_function("()=>window.__pret===true", timeout=120000); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{document.querySelectorAll('figure').forEach((f,i)=>{if(i>0)f.remove();});}")
    fr=pg.query_selector('.fr[data-vif]'); fr.scroll_into_view_if_needed(); pg.wait_for_timeout(400)
    bb=fr.bounding_box()
    cap=pg.query_selector('.fr .prise'); cb=cap.bounding_box()
    TX, TY = cb['x']+90, cb['y']+215
    RX = int((TX-bb['x'])*2)-70; RY=int((TY-bb['y'])*2)-70
    CLIP={'x':bb['x'],'y':bb['y'],'width':390,'height':470}
    ZOOM={'x':bb['x']+40,'y':bb['y']+150,'width':180,'height':150}
    print('erreurs :', errs[:3])
    def shot(nom, clip=None): pg.screenshot(path='%s/%s.png'%(DOSS,nom), clip=clip or CLIP)
    def tenir(v):
        pg.evaluate("""(v)=>{window.__tenir=true;
          const f=document.querySelector('.fr[data-vif]');
          (function t(){ if(!window.__tenir) return; f.__vlac=v; requestAnimationFrame(t); })();}""", v)
    def lacher(): pg.evaluate("()=>{window.__tenir=false;}")
    def arret(): pg.evaluate("()=>{VUE_AUTO=0;}")
    def repart(): pg.evaluate("()=>{VUE_AUTO=6.2832/(VUE_T/1000);}")

    # ── A · LE DOIGT POSÉ ───────────────────────────────────────────────────
    arret(); pg.wait_for_timeout(300)
    shot('A0_avant')
    pg.mouse.move(TX,TY); pg.mouse.down()
    pg.wait_for_timeout(60);   shot('A1_pose')
    pg.wait_for_timeout(440);  shot('A2_tenu05')
    pg.mouse.up()
    pg.wait_for_timeout(500);  shot('A3_lache05')
    pg.wait_for_timeout(1000); shot('A4_lache15')
    pg.wait_for_timeout(2000); shot('A5_lache35')
    pg.wait_for_timeout(1500)

    # ── B · UNE ROTATION LANCÉE, la vitesse ENTRETENUE pendant la capture ───
    repart(); pg.wait_for_timeout(600)
    shot('B0_repos'); shot('Z0_repos', ZOOM)
    tenir(6); pg.wait_for_timeout(400)
    cpt=pg.evaluate("()=>window._compteTr()")
    om=pg.evaluate("()=>+document.querySelector('.fr[data-vif]').__om.toFixed(2)")
    shot('B1_rotation'); shot('Z1_rotation', ZOOM)
    lacher(); pg.wait_for_timeout(4000)

    # ── C · UN CRATÈRE, PUIS UN LANCER — sans que le doigt repasse dessus ───
    # ⚠ ON REMET LA VUE OÙ ELLE ÉTAIT AVANT DE PHOTOGRAPHIER. Sinon on mesure la
    #   rotation (matière différente sous la fenêtre, et densité divisée par le saut
    #   de vitesse) au lieu de mesurer le comblement. La question est : « après avoir
    #   lancé, le creux est-il encore là ? » — donc on revient au même point de vue.
    arret(); pg.wait_for_timeout(300)
    def creuse():
        pg.mouse.move(TX,TY); pg.mouse.down(); pg.wait_for_timeout(420); pg.mouse.up()
        pg.wait_for_timeout(120)
    def remets(lac0):
        pg.evaluate("""(l)=>{const f=document.querySelector('.fr[data-vif]');
          f.__vlac=0; f.__om=0; f.__lac=l; orbitePose(f, f.__u||0);}""", lac0)
        pg.wait_for_timeout(220)
    lac0=pg.evaluate("()=>document.querySelector('.fr[data-vif]').__lac")
    creuse(); shot('C0_creux')
    pg.wait_for_timeout(350); remets(lac0); shot('C1_sans_lancer')
    pg.wait_for_timeout(4500)
    remets(lac0)
    creuse(); shot('C2_creux')
    pg.evaluate("()=>{document.querySelector('.fr[data-vif]').__vlac=9;}")
    pg.wait_for_timeout(350)
    remets(lac0); shot('C3_avec_lancer')
    pg.close()

    # ── LA MESURE, SUR LES IMAGES ───────────────────────────────────────────
    m=b.new_page(); m.goto('http://127.0.0.1:8752/scratchpad/mesure_png.html')
    m.wait_for_function("()=>window.__pret===true", timeout=30000)
    def mes(nom,x,y,w,h):
        return m.evaluate("([u,x,y,w,h])=>window.mesure(u,x,y,w,h)",
                          ['/%s/%s.png'%(DOSS,nom),x,y,w,h])
    print('\n── A · LE DOIGT POSÉ (rotation arrêtée) — carré de 140 px au point touché')
    print('   %-14s %8s %8s' % ('image','encre','part allumée'))
    for n in ['A0_avant','A1_pose','A2_tenu05','A3_lache05','A4_lache15','A5_lache35']:
        r=mes(n,RX,RY,140,140); print('   %-14s %8.2f %7.2f %%' % (n, r['moy'], r['part']))
    print('\n── B · LA ROTATION (vitesse entretenue à %.1f rad/s pendant la capture)' % om)
    print('   %d grains peints, %d tampons de traînée' % (cpt['grains'], cpt['trainees']))
    print('   (mouvement HORIZONTAL : runH doit dépasser runV)')
    print('   %-14s %8s %8s %8s %8s %8s' % ('image','encre','part','runH','runV','runH/runV'))
    for n in ['B0_repos','B1_rotation']:
        r=mes(n,120,260,540,420)
        print('   %-14s %8.2f %7.2f %% %7.2f %7.2f %8.3f'
              % (n, r['moy'], r['part'], r['runH'], r['runV'], r['runH']/r['runV']))
    print('\n── C · LE CRATÈRE, AVEC ET SANS LANCER (0,35 s après le lâcher, MÊME point de vue)')
    for n,t in [('C0_creux','le creux'),('C1_sans_lancer','+0,35 s SANS lancer'),
                ('C2_creux','le même creux'),('C3_avec_lancer','+0,35 s AVEC lancer')]:
        r=mes(n,RX,RY,140,140); print('   %-16s %-22s %8.2f %7.2f %%' % (n,t,r['moy'],r['part']))
    b.close()

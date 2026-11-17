"""v206 §0 — la planche de captures de référence : chaque écran (la liste de redteam_app, Studio compris), clair et sombre,
échelles 1 (430×932) et 0,79 (330×714). Le même hasard (graine 777) que redteam_app, Toile de 10 paroles (banc_tom.toile_pleine).
python3 scratchpad/v206/captures_ref.py <dossier> [--fichier=app.html]"""
import sys, os, re; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image, ImageDraw
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
F = next((a.split('=', 1)[1] for a in sys.argv[2:] if a.startswith('--fichier=')), 'app.html')
src = open('redteam_app.py', encoding='utf-8').read()
ns = {'VITE': False}; exec(re.search(r'(def ecrans\(pg\):.*?return L\n)', src, re.S).group(1), ns); ecrans = ns['ecrans']
HASARD = "(()=>{let a=777; Math.random=function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return ((t^t>>>14)>>>0)/4294967296;};})()"
planches = []
with sync_playwright() as p:
    b = p.webkit.launch()
    for vue in ('1', '079'):
        for th in ('clair', 'sombre'):
            vw, vh = (430, 932) if vue == '1' else (330, 714)
            ctx = B.contexte(b, sombre=(th == 'sombre'), vw=vw, vh=vh); B.toile_pleine(ctx, 10); ctx.add_init_script(HASARD)
            pg = B.ouvre(ctx, F); faits = []
            for nom, js in ecrans(pg):
                pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); }catch(e){} try{ closeAll(); }catch(e){} document.querySelectorAll('#auraScreen.show .closeb, #studioScreen.show .closeb').forEach(x=>{ if(x.getBoundingClientRect().top<300) x.click(); }); }")
                pg.wait_for_timeout(700)
                try: pg.evaluate(js)
                except Exception as e: print('  !', nom, str(e)[:100])
                pg.wait_for_timeout(2600)
                ch = os.path.join(OUT, '%s-%s-%s.png' % (vue, th, nom.replace(' ', '_').replace('+', 'plus')))
                B.capture(pg, ch); faits.append((nom, ch)); print(vue, th, nom, flush=True)
            ctx.close(); planches.append(('%s-%s' % (vue, th), faits))
    b.close()
for titre, faits in planches:   # une planche par vue et par thème : 6 colonnes
    ims = [Image.open(c).convert('RGB') for _, c in faits]; w = 260; h = int(ims[0].height * w / ims[0].width)
    col = 6; lig = (len(ims) + col - 1) // col; P = Image.new('RGB', (col * (w + 10) + 10, lig * (h + 34) + 10), (240, 236, 228)); d = ImageDraw.Draw(P)
    for i, (im, (nom, _)) in enumerate(zip(ims, faits)):
        x = 10 + (i % col) * (w + 10); y = 10 + (i // col) * (h + 34); P.paste(im.resize((w, h)), (x, y + 20)); d.text((x, y + 4), nom, fill=(20, 20, 20))
    P.save(os.path.join(OUT, 'PLANCHE-%s.png' % titre))
print('fin', len(planches))

# Les numéros du jeu sont-ils STABLES d'un chargement à l'autre ? (chantiers 71 et 72)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br = p.chromium.launch()
    for k in range(4):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        print(k + 1, pg.evaluate("""()=>({crepes:(promises.find(q=>q.title==='faire les crêpes')||{}).id, statut:(promises.find(q=>q.title==='faire les crêpes')||{}).status,
            n:promises.length, min:Math.min(...promises.map(q=>q.id)), max:Math.max(...promises.map(q=>q.id)), nid:(typeof nid!=='undefined'?nid:null), jeu:window._jeuPlanche, win:typeof window.promises})"""))
        pg.context.close()
    br.close()

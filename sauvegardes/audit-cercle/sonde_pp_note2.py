# SONDE 2 : la séquence EXACTE du relevé (fiche, puis page + « invite », puis page + « long ») — la hauteur de la zone dans le temps.
from playwright.sync_api import sync_playwright
LONG = "prévenir Rachel la veille, apporter le gâteau et les bougies, et passer chercher Maman à la gare"
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
PP = [(BASE, 200), ("()=>document.getElementById('createBtn').click()", 600),
      ("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}", 900),
      ("()=>document.getElementById('csBotBar').click()", 1800)]
ETAT = """()=>{ const z=document.querySelector('#createSheet .s2-zone'); if(!z) return 'pas de zone'; if(!z.__n) z.__n = (window.__k=(window.__k||0)+1);
  const ta=z.querySelector('textarea'); return {zone_n:z.__n, h:z.getBoundingClientRect().height/(document.getElementById('device').getBoundingClientRect().width/390), zstyle:z.getAttribute('style'), lignes:z.getAttribute('data-cercle-lignes'), ta:ta&&ta.id, taH:ta&&ta.style.height, val:ta&&ta.value.length, pp:document.getElementById('createSheet').classList.contains('pp-peauf')}; }"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width':430,'height':932}, device_scale_factor=2).new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setTheme('dark')"); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
    for passe in ('invite', 'long'):
        for js, w in PP: pg.evaluate(js); pg.wait_for_timeout(w)
        print('--', passe, 'ouvert', pg.evaluate(ETAT))
        if passe == 'long':
            pg.evaluate("(t)=>{ document.querySelectorAll('#detailPoster .s2-zone textarea, #createSheet .s2-zone textarea').forEach(x=>{ x.value=t; x.dispatchEvent(new Event('input',{bubbles:true})); }); }", LONG)
            prev = 0
            for d in (0, 100, 300, 700, 1500):
                pg.wait_for_timeout(d if d == 0 else d - prev); prev = d
                print('   +%d ms' % d, pg.evaluate(ETAT))
            for k in range(3):
                pg.evaluate("(k)=>{const c=document.querySelector('#createSheet .dpd-corps')||document.querySelector('#createSheet'); c.scrollTop=k*240;}", k); pg.wait_for_timeout(260)
                print('   défilé %d' % k, pg.evaluate(ETAT))
        prev = 0
    br.close()

import io, sys
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 892}, device_scale_factor=2, has_touch=True)
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/promi-invite-variantes.html'); pg.wait_for_timeout(9000)
    ims = []
    for v in ('A', 'B'):
        pg.evaluate("(v)=>{ _invite.v(v); _invite.ouvre(); }", v); pg.wait_for_timeout(1150 + 900 + (500 if v == 'A' else 520))
        ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x': 0, 'y': 48 + 150, 'width': 390, 'height': 200}))))
    # un toucher sur la fiche : rien ne se trace
    pg.touchscreen.tap(300, 48 + 290); pg.wait_for_timeout(300)
    for i in range(6): pg.mouse.move(150 + 30 * i, 48 + 290)
    st = pg.evaluate("()=>{ const w=_invite.cadre().contentWindow; return w.eval('promises.filter(q=>q.title===\"écrire à Lou\").map(q=>q.status)'); }")
    print('statut', st, 'etat', pg.evaluate("()=>_invite.etat()"))
    w, h = ims[0].size; o = Image.new('RGB', (w, h * 2 + 10), (255, 255, 255)); o.paste(ims[0], (0, 0)); o.paste(ims[1], (0, h + 10)); o = o.resize((o.width // 2, o.height // 2)); o.save('scratchpad/v148/invite_AB.png')
    b.close()

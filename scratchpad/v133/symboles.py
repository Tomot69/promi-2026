from playwright.sync_api import sync_playwright
from PIL import Image
A='<path d="M15 3l6 6L11 19l-6-6z"/><path d="M5 13l-1.6 4.6 3 3L11 19"/><path d="M12.2 5.8l6 6"/>'
B='<path d="M17.5 13.5V18a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8.5a2 2 0 0 1 2-2h4.5"/><path d="M10.5 15.5l.8-3.2 7.9-7.9a1.7 1.7 0 0 1 2.4 2.4l-7.9 7.9-3.2.8z"/>'
C='<rect x="3.5" y="5" width="17" height="14" rx="2.5"/><path d="M1.5 14.5c2.6-5 5.2-5 7.2-1.6s4.4 3.4 6.4 0 4-4.4 7.4-3.4"/>'
ACT='<path d="M4 8.5h3l1.5-2.2h7L17 8.5h3a1.5 1.5 0 0 1 1.5 1.5v8A1.5 1.5 0 0 1 20 19.500H4A1.5 1.5 0 0 1 2.5 18v-8A1.5 1.5 0 0 1 4 8.5z"/><circle cx="12" cy="13.5" r="3.4"/>'
def svg(d,px): return '<svg viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</svg>'%(px,px,d)
NAT=[('Promi','#82AEF8'),('Chiche','#FFB8D2'),('Cercle','#C9A8F5')]
def bloc(th):
    fond={'clair':'#F7F0DE','sombre':'#050302'}[th]; enc={'clair':'#201908','sombre':'#F7F0DE'}[th]
    bord={'clair':'rgba(32,25,8,.34)','sombre':'rgba(247,240,222,.42)'}[th]; bg={'clair':'rgba(247,240,222,.22)','sombre':'rgba(32,25,8,.18)'}[th]
    h='<div style="background:%s;color:%s;padding:26px 24px 30px;width:780px;box-sizing:border-box"><div style="font:700 15px Gilbert,system-ui;letter-spacing:.06em;text-transform:uppercase;margin-bottom:18px">%s</div>'%(fond,enc,th)
    h+='<div style="display:grid;grid-template-columns:150px repeat(4,1fr);gap:14px 10px;align-items:center;font:500 13px Atkinson,system-ui">'
    h+='<div></div>'+''.join('<div style="text-align:center;font:700 13px Gilbert,system-ui;text-transform:uppercase;letter-spacing:.04em">%s</div>'%t for t in ('Aujourd’hui','A · le feutre','B · la plume sur le cadre','C · le cadre et le trait'))
    h+='<div>le symbole, agrandi (×5)</div>'+''.join('<div style="display:flex;justify-content:center">%s</div>'%svg(d,85) for d in (ACT,A,B,C))
    for n,c in NAT:
        h+='<div>sur la bande d’un %s<br>taille réelle (34 pt)</div>'%n
        for d in (ACT,A,B,C):
            h+='<div style="background:%s;height:64px;display:flex;align-items:center;justify-content:center;border-radius:12px"><span style="width:34px;height:34px;box-sizing:border-box;border:1.5px solid %s;border-radius:50%%;background:%s;display:flex;align-items:center;justify-content:center;color:%s;opacity:.62">%s</span></div>'%(c,bord,bg,'#201908' if th=='clair' else '#F7F0DE',svg(d,17))
    h+='<div>à l’encre pleine<br>(×2, sans le voile)</div>'+''.join('<div style="background:#82AEF8;height:92px;display:flex;align-items:center;justify-content:center;border-radius:12px"><span style="width:68px;height:68px;box-sizing:border-box;border:3px solid #201908;border-radius:50%%;display:flex;align-items:center;justify-content:center;color:#201908">%s</span></div>'%svg(d,34) for d in (ACT,A,B,C))
    return h+'</div></div>'
H='<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="planche-polices.css"><body style="margin:0;background:#fff"><div id="p" style="width:780px"><div style="padding:22px 24px 14px;font:700 19px Gilbert,system-ui;text-transform:uppercase;letter-spacing:.04em;color:#201908">v133 · C-060 — le symbole du bouton photo : trois propositions<div style="font:400 13px Atkinson,system-ui;text-transform:none;letter-spacing:0;margin-top:6px">Trait plein de 2, bouts ronds, la grammaire des icônes de fiche. Le bouton garde sa place, sa taille (34 pt) et son contour.</div></div>'+bloc('clair')+bloc('sombre')+'</div>'
open('zz-symboles.html','w',encoding='utf-8').write(H)
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(viewport={'width':780,'height':900},device_scale_factor=3); pg.goto('http://127.0.0.1:8752/zz-symboles.html'); pg.wait_for_timeout(1500)
    pg.locator('#p').screenshot(path='planche-v133/symboles.png'); b.close()
P=Image.open('planche-v133/symboles.png'); P.resize((1290,int(P.height*1290/P.width))).save('planche-v133/symboles-tel.png'); print(P.size)

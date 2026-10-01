from playwright.sync_api import sync_playwright
JS=r"""()=>{
  const ids=['detailPoster','indexSheet','createSheet','feedView','shareScreen','auraScreen',
             'studioScreen','settingsScreen','essaimSheet','plusScreen','stage','toile'];
  const o={};
  ids.forEach(id=>{const e=document.getElementById(id);
    if(!e){o[id]='ABSENT';return;}
    const ch=[]; let p=e.parentElement;
    while(p && p!==document.body){ ch.push(p.id?('#'+p.id):('.'+(p.className+'').split(' ').filter(Boolean)[0])); p=p.parentElement; }
    o[id]={chaine:ch.join(' < '),
           sousDevice: !!document.querySelector('#device #'+id),
           sousFrame:  !!document.querySelector('.frame #'+id)};});
  o['_device'] = (function(){const d=document.getElementById('device');
    if(!d) return 'ABSENT'; let p=d.parentElement, ch=[];
    while(p && p!==document.body){ ch.push(p.id?('#'+p.id):('.'+(p.className+'').split(' ').filter(Boolean)[0])); p=p.parentElement; }
    return {classes:d.className, chaine:ch.join(' < ')};})();
  return o;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    o=pg.evaluate(JS)
    print('#device :', o.pop('_device'))
    print()
    for k,v in o.items():
        if v=='ABSENT': print('%-16s ABSENT'%k); continue
        marque = 'sous #device' if v['sousDevice'] else ('SOUS .frame SEULEMENT' if v['sousFrame'] else '?')
        print('%-16s %-24s %s'%(k, marque, v['chaine'][:70]))
    b.close()

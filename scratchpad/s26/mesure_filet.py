from playwright.sync_api import sync_playwright
import json
JS = r"""
()=>{
  var out=[];
  document.querySelectorAll('#auraScreen canvas.kr-c').forEach(function(cv,i){
    if(i>2) return;
    var g=cv.getContext('2d'), W=cv.width, H=cv.height, cx=W/2, cy=H/2;
    var d=g.getImageData(0,0,W,H).data;
    function px(x,y){var o=(y*W+x)*4; return [d[o],d[o+1],d[o+2],d[o+3]];}
    // rayon vers la droite (0 deg) puis vers le haut-droit
    var prof=[];
    for(var r=0;r<cx;r+=0.5){
      var x=Math.round(cx+r), y=Math.round(cy);
      if(x>=W) break;
      prof.push([+r.toFixed(1), px(x,y)]);
    }
    // resume : premier et dernier r ou alpha>20, et ou la couleur est creme
    var first=null,last=null,cf=null,cl=null;
    prof.forEach(function(p){
      var c=p[1];
      if(c[3]>20){ if(first===null)first=p[0]; last=p[0]; }
      var creme = Math.abs(c[0]-247)<14 && Math.abs(c[1]-240)<14 && Math.abs(c[2]-222)<16 && c[3]>120;
      if(creme){ if(cf===null)cf=p[0]; cl=p[0]; }
    });
    var b=cv.getBoundingClientRect();
    out.push({i:i, W:W, boxW:+b.width.toFixed(2), R:W*window.KR_R, lw:W*window.KR_LW,
              ringOut:+(W*window.KR_R+W*window.KR_LW/2).toFixed(2), demiW:+(W/2).toFixed(2),
              peintFirst:first, peintLast:last, cremeFirst:cf, cremeLast:cl});
  });
  return out;
}
"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
    pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5400)
    print(json.dumps(pg.evaluate(JS), indent=1, ensure_ascii=False))
    open('scratchpad/s26/aura-dark.png','wb').write(pg.query_selector('#device').screenshot())
    b.close()

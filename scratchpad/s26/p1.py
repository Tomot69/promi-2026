import io
S=io.open('app.html',encoding='utf-8').read()

old = """function _poseFilet(){ if(!_krFilet) return;
  var _bw=(cv.getBoundingClientRect&&cv.getBoundingClientRect().width)||W;
  var _fw=1.4*(W/(_bw||W));
  g.save(); g.lineWidth=_fw; g.lineCap='butt'; g.strokeStyle='#F7F0DE';
  g.beginPath(); g.arc(cx,cy,W/2-_fw/2,0,6.2832); g.stroke(); g.restore(); }"""
new = """/* ⛑ 23 SEPTEMBRE 2026, cinquième écriture (Tom) — « LE FILET DOIT ÊTRE COLLÉ AU BORD
   EXTÉRIEUR DU DISQUE. Aujourd'hui il y a un écart. Il cerne le bord, sans jeu. »
   Il était posé au bord du CANEVAS (`W/2`), pas au bord de l'ANNEAU. Les deux ne coïncident
   que chez le poseur de fiche, qui force `KR_R=(D−EP)/2/D` et `KR_LW=EP/D` : là,
   `R+lw/2 = W/2`, et le filet tombait juste. Partout ailleurs — l'Aura, la fiche d'une
   personne — les constantes globales valent `KR_R .33` et `KR_LW 12/78` : le bord de
   l'anneau est à **0,4069·W**, le filet était à **0,5·W**. Mesuré sur les Noyaux de
   l'Aura (canevas 104) : anneau jusqu'à **42,3**, crème de **50,5 à 51** — **8,2 px de jeu**,
   soit 4,1 px à l'écran. Le filet suit donc LE BORD PEINT (`_krDehors`, que l'anneau
   extérieur du Cercle relève quand il existe), borné au canevas pour ne pas être rogné. */
function _poseFilet(){ if(!_krFilet) return;
  var _bw=(cv.getBoundingClientRect&&cv.getBoundingClientRect().width)||W;
  var _fw=1.4*(W/(_bw||W));
  var _rf=Math.min(_krDehors+_fw/2, W/2-_fw/2);
  g.save(); g.lineWidth=_fw; g.lineCap='butt'; g.strokeStyle='#F7F0DE';
  g.beginPath(); g.arc(cx,cy,_rf,0,6.2832); g.stroke(); g.restore();
  try{ cv.setAttribute('data-filet',[(_krDehors).toFixed(2),_rf.toFixed(2),_fw.toFixed(2)].join(',')); }catch(_){} }
var _krDehors=R+lw/2;   /* le bord EXTERIEUR de ce qui est peint — l'anneau, ou celui du Cercle */"""
assert S.count(old)==1, "A"
S=S.replace(old,new)

oldB="_arcs(org2,oR);}}"
assert S.count(oldB)==1, "B %d"%S.count(oldB)
S=S.replace(oldB,"_arcs(org2,oR);_krDehors=Math.max(_krDehors,oR+olw/2);}}")

# le + de l'accueil : l'anneau y est `inset:0`, donc son bord exterieur EST le bord de la boite
oldC="#createBtn.dhero{outline:1px solid var(--c-creme95)!important;outline-offset:3px!important}"
assert S.count(oldC)==1, "C"
newC=("/* ⛑ 23 SEPTEMBRE 2026, second tour (Tom) — L'ÉCART VENAIT DE L'OFFSET. Le `3px` avait été\n"
 "   calculé sur `.dhero::before{inset:-3px}` — la règle GÉNÉRALE. Mais sur l'accueil c'est\n"
 "   `#device .acc-barre #createBtn::before{inset:0!important}` qui gagne : l'anneau s'arrête au\n"
 "   bord de la boîte, et l'outline se posait donc **3 px plus loin**. Offset 0 = collé. */\n"
 "#createBtn.dhero{outline:1px solid var(--c-creme95)!important;outline-offset:0!important}")
S=S.replace(oldC,newC)
io.open('app.html','w',encoding='utf-8').write(S)
print("ok")

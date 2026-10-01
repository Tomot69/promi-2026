# Lot v16 — décision 3 : en sombre, chaque arc d'état garde SA valeur exacte et prend le filet
# crème de 1,4 px, collé à son bord (dans sa propre empreinte : l'arc se resserre de 1,4 de
# chaque côté et à chaque bout, la crème occupe ce qui reste). Condition : ce qui est peint SOUS
# l'anneau (_krFilet, déjà calculé par le peintre), jamais une classe.
import io
F='app.html'; S=io.open(F,encoding='utf-8').read()
a="""    if(a1<=a0) continue;
    g.strokeStyle='rgb('+rgx[i].c.join(',')+')'; g.beginPath(); g.arc(cx,cy,RR,a0,a1); g.stroke(); }
}"""
b="""    if(a1<=a0) continue;
    if(_krFilet){ var _fwA=1.4*_sc, _lw0=g.lineWidth, _dA=_fwA/RR;
      g.save(); g.strokeStyle='#F7F0DE'; g.beginPath(); g.arc(cx,cy,RR,a0,a1); g.stroke();
      if(a1-_dA>a0+_dA && _lw0>2*_fwA){ g.lineWidth=_lw0-2*_fwA; g.strokeStyle='rgb('+rgx[i].c.join(',')+')';
        g.beginPath(); g.arc(cx,cy,RR,a0+_dA,a1-_dA); g.stroke(); }
      g.restore(); continue; }
    g.strokeStyle='rgb('+rgx[i].c.join(',')+')'; g.beginPath(); g.arc(cx,cy,RR,a0,a1); g.stroke(); }
}"""
assert S.count(a)==1; S=S.replace(a,b)
io.open(F,'w',encoding='utf-8').write(S); print('ok')

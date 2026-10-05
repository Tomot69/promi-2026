import io
S=io.open('redteam_decoupe.py',encoding='utf-8').read()
old="""          for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; if(Math.max(Math.abs(d[i]-c[0]),Math.abs(d[i+1]-c[1]),Math.abs(d[i+2]-c[2]))>48) au++; }"""
new="""          /* ⚑ v131 (C-048) — LA « DALLE À 3,11 % » ÉTAIT DU JUGE. Reproduite en boucle (zz-v130, cinquante passages) : une dalle Tesselle
             rendue avec une RAMPE (`opts.rampe`, Q30 : la luminosité remappée sur les trois tons de la nature) — l'ombre de ses carreaux
             prend le ton sombre de la rampe, à plus de 48 du ton dominant. Ce sont SES couleurs, pas un morceau de voisine. Une couleur
             qui tombe sur la rampe déclarée (ses tons et leurs intermédiaires) n'est donc pas « une autre couleur ». */
          const RP=[]; try{ const cs=opts&&opts.rampe&&opts.rampe.cols; if(cs&&cs.length>1){ for(let a=0;a<cs.length-1;a++) for(let u=0;u<=12;u++){ const t=u/12; RP.push([cs[a][0]+(cs[a+1][0]-cs[a][0])*t, cs[a][1]+(cs[a+1][1]-cs[a][1])*t, cs[a][2]+(cs[a+1][2]-cs[a][2])*t]); } } }catch(e){}
          for(let i=0;i<d.length;i+=4){ if(d[i+3]<250) continue; if(Math.max(Math.abs(d[i]-c[0]),Math.abs(d[i+1]-c[1]),Math.abs(d[i+2]-c[2]))>48){
              let sur=false; for(let q=0;q<RP.length&&!sur;q++){ if(Math.max(Math.abs(d[i]-RP[q][0]),Math.abs(d[i+1]-RP[q][1]),Math.abs(d[i+2]-RP[q][2]))<=30) sur=true; }
              if(!sur) au++; } }"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('redteam_decoupe.py','w',encoding='utf-8').write(S)

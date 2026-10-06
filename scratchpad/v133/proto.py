import io,sys
K0,K1=float(sys.argv[1]),float(sys.argv[2])
M=io.open('promi-moteur.js',encoding='utf-8').read()
a="function _amplifie(){ if(!_semisNeuf()) return; var a=avg();"
assert M.count(a)==1
M=M.replace(a,"""function _amplifie(){ var a=avg();
  if(!_semisNeuf()){ /* PROTOTYPE v133 (C-062), hors app : l'ampleur stable de chaque parole, étendue aux anciens mondes */
    for(var i0=0;i0<seeds.length;i0++){ var s0=seeds[i0]; if(s0.part!=null||s0.pid==null||s0.kind==='nuee') continue; var d0=_ampleur(s0); if(d0==null) continue;
      var u0=Math.sqrt(Math.max(0,(d0+0.09)/0.31)), f0=3.4+(%s+%s*u0*u0*u0*u0)*a; s0.wFin=f0; if(!s0.wAt){ s0.wt=f0; if(s0._amp==null) s0.w=f0; } s0._amp=1; } return; }"""%(K0,K1))
b="""      autoView();
      kick();
      return;"""
assert M.count(b)==1, M.count(b)
M=M.replace(b,"""      _amplifie(); relax(); relax();
      autoView();
      kick();
      return;""")
io.open('zz-moteur-v133.js','w',encoding='utf-8').write(M)
S=io.open('app.html',encoding='utf-8').read(); t='<script src="promi-moteur.js"></script>'; assert S.count(t)==1
io.open('zz-v133.html','w',encoding='utf-8').write(S.replace(t,'<script src="zz-moteur-v133.js"></script>'))

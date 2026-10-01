import io
F='app.html'; S=io.open(F,encoding='utf-8').read()
a="""  var t=e.target.closest&&e.target.closest('#cguCard,#delAccount');
  if(!t)return;
  if(t.id==='cguCard'){ if(window.toast)toast('Conditions d\\u2019utilisation'); return; }
  /* la suppression demande une confirmation : elle est irreversible. */
  if(window.confirm && !confirm('Supprimer ton compte et tous tes Promi ?\\n'+
     'Cette action est definitive.')) return;
  try{ localStorage.clear(); }catch(_){}
  location.reload();"""
b="""  var t=e.target.closest&&e.target.closest('#cguCard,#delAccount');
  if(!t)return;
  /* ⚑ v16 : les deux lignes passent par lot-V16 — une page « bientôt disponible » propre, et une
     suppression qui demande confirmation puis laisse quelques secondes pour annuler. */
  e.stopPropagation();
  if(t.id==='cguCard'){ if(window._v16Legal) window._v16Legal('cgu'); return; }
  if(window._v16SupprimerCompte) window._v16SupprimerCompte();"""
assert S.count(a)==1; S=S.replace(a,b)
io.open(F,'w',encoding='utf-8').write(S); print('ok')

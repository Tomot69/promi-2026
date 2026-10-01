# CHANTIER 70 — la page + rebâtit la liste de son Peaufiner sans cesse (et un toucher se perd). Comparer avant d'agir (§8).
import hashlib, io, os
F = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app.html'))
S = io.open(F, encoding='utf-8').read(); avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == 'aedf74fe2e81ab7df9b7a3c44286d673', avant
def remplace(old, new):
    global S
    assert S.count(old) == 1, 'motif absent ou multiple : ' + old[:80]
    S = S.replace(old, new)
# 1 · la signature de ce qu'on va bâtir, et on ne rebâtit que si elle change (ou si un contrôle emprunté est reparti)
remplace("""      var liste = corps.querySelector('.s2-liste');
      if(!liste){ liste = B.el('div','s2-liste'); corps.appendChild(liste); }
      /* tout contrôle emprunté rentre chez lui AVANT qu'on vide la liste : sans ça,""",
"""      var liste = corps.querySelector('.s2-liste');
      if(!liste){ liste = B.el('div','s2-liste'); corps.appendChild(liste); }
      /* ⚑ CHANTIER 70 — COMPARER AVANT D'AGIR (CLAUDE §8). `tout()` repasse ici à chaque repeinte (les minuteries du pinceau
         0/120/400/900/1800 ms, après chaque clic 80/260/600 ms, l'observateur de classe) et la liste était VIDÉE PUIS REBÂTIE
         à chaque fois, sans que rien n'ait changé : mesuré, six zones neuves en 2,5 s, et un toucher sur l'encart du mur perdu
         quand le nœud était remplacé entre l'appui et le relâcher (2 sur 40, chantier 70). On calcule la SIGNATURE de ce qu'on
         va bâtir — nature, titre, à qui, échéance, Nuée, fichiers, compagnon, membres — et on ne rebâtit que si elle change,
         ou si un contrôle emprunté n'est plus dans la liste (il a été rendu à l'app à la fermeture). */
      var _P = window._phrase || {}, _sig = '';
      try{
        _sig = JSON.stringify([n, (_P.titre||'').trim(), (n==='nuee'?((document.getElementById('nName')||{}).value||''):''),
          (n!=='nuee'?aQui():''), (n!=='nuee'?motEcheance():''), ((n!=='nuee'&&n!=='chiche')?nomNuee():''), (_P.avec||''),
          ((document.getElementById('csFiles')||{}).childElementCount||0), (window.newNueeMembers||[]).join('|'),
          ((document.getElementById('nFirstList')||{}).childElementCount||0)]);
      }catch(_){ _sig = ''; }
      var _pris = document.getElementById(n === 'nuee' ? 'nMembers' : 'fNote');
      if(_sig && liste.getAttribute('data-pp-sig') === _sig && liste.firstChild && _pris && liste.contains(_pris)) return;
      liste.setAttribute('data-pp-sig', '');
      /* tout contrôle emprunté rentre chez lui AVANT qu'on vide la liste : sans ça,""")
# 2 · la signature est posée quand la liste est ENTIÈREMENT bâtie (Nuée, puis Promi / Chiche)
remplace("""        liste.appendChild(B.reg('LES PROMI DE LA NU\\u00c9E', np+' Promi', {hote:B.emprunte('nFirst')}));
        return;""",
"""        liste.appendChild(B.reg('LES PROMI DE LA NU\\u00c9E', np+' Promi', {hote:B.emprunte('nFirst')}));
        liste.setAttribute('data-pp-sig', _sig);
        return;""")
remplace("""      liste.appendChild(B.reg('PI\\u00c8CES JOINTES', nf+' fichier'+(nf>1?'s':''),
        {cls:'s2-vis2', vis:mvs, hote:B.emprunte('csFiles')}));""",
"""      liste.appendChild(B.reg('PI\\u00c8CES JOINTES', nf+' fichier'+(nf>1?'s':''),
        {cls:'s2-vis2', vis:mvs, hote:B.emprunte('csFiles')}));
      liste.setAttribute('data-pp-sig', _sig);""")
io.open(F, 'w', encoding='utf-8').write(S); print('avant', avant, '→ après', hashlib.md5(S.encode('utf-8')).hexdigest())

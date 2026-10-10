#!/usr/bin/env python3
"""
redteam_volume.py — LA PELOTE EST LE SEUL VOLUME DE L'APP (Tom, v114, 30 sept. 2026). Contrôle STATIQUE, sans navigateur.

Un halo, une ombre, un dégradé ne sont autorisés que dans le composant de la Pelote de l'Aura — LISTE BLANCHE NOMINATIVE :
le bloc `lot-V114-PELOTE-css` (#auPeloteHalo, #auPeloteOmbre). On balaie app.html et promi-moteur.js à la recherche de :
  radial-gradient( · linear-gradient( · conic-gradient( · repeating-*-gradient( · createRadialGradient · createLinearGradient ·
  createConicGradient · shadowBlur · shadowColor · drop-shadow( · text-shadow (avec flou) · box-shadow (avec flou, hors inset)
Chaque occurrence est nommée par son fichier, le bloc (lot) qui la contient et 70 caractères de contexte.

LA DETTE DE NAISSANCE — ce qui existait avant la règle — est inscrite dans `volume-dette.json`, écrite UNE fois (`--figer`),
jamais pour faire passer : elle NOMME chaque occurrence ancienne (le fond de la Toile `_fondVif` en fait partie) ; elle se
solde à la main, et toute occurrence NOUVELLE hors liste blanche fait échouer.
Preuve que le juge mord : `--sonde` pose un halo (shadowBlur) sur une dalle de la Toile dans une copie du moteur → il doit rougir.
v119 : `--sonde=mini` pose le mini halo de la Pelote sur une dalle → il doit rougir.
Usage : python3 redteam_volume.py [--figer] [--sonde | --sonde=halo | --sonde=mini]
Originaux : sauvegardes/redteam_volume-avant-v118.py, -avant-v119.py
"""
import io, os, re, sys, json, collections
ICI=os.path.dirname(os.path.abspath(__file__))
# LISTE BLANCHE NOMINATIVE — (bloc → motifs permis). v115 : le halo flou devient la COURONNE de fibres ; son peintre,
# window._couronnePelote, est un VOLUME lui aussi : il n'est permis que dans son bloc et à son unique appel (l'Aura).
# v119 (Tom) : l'écho de v118 est RETIRÉ (refusé, comme la couronne et le halo flou). La mise en valeur est un MINI HALO qui prolonge
# la lumière de la Pelote, et une ombre portée (en sombre : une flaque de lumière dont l'ombre est le creux). Leurs deux peintres
# (window._haloPelote, window._flaquePelote) ne sont permis que dans leur bloc et à leur unique appel (l'Aura).
# ⚑ v137 (Tom, 8 oct. 2026, C-071) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_volume-avant-v137.py) : « Le halo et l'ombre de la Pelote
# sortent de la liste blanche des exceptions. Il ne reste que le flou des murs de Ma Parole !. […] plus aucun effet autour de la Pelote. »
# LA LISTE BLANCHE EST VIDE : la Pelote n'a plus ni halo, ni ombre, ni couronne, ni flaque — et leurs peintres ne doivent plus exister.
# (Le flou des murs de Ma Parole ! est un `filter:blur`, que ce juge n'a jamais compté : il est jugé par redteam_murs.)
# ⚑ v139 (Tom, 9 oct. 2026, C-083) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_volume-avant-v139.py) : « L'ombre revient, sous la Pelote, dans
# les deux thèmes (géométrie de v121). Rien d'autre autour : ni halo, ni liseré. » LA LISTE BLANCHE PORTE UNE SEULE EXCEPTION, NOMINATIVE :
# le bloc `lot-V139-OMBRE-css` (l'ombre, clair et sombre : deux dégradés, pas un de plus). Le halo, la couronne, la flaque restent interdits.
BLANCHE={'lot-V139-OMBRE-css':'*'}
OMBRE_ATTENDUE=2
def permis(lot, motif):
    b=BLANCHE.get(lot); return b=='*' or (b is not None and any(motif.startswith(m) for m in b))
MOTIFS=re.compile(r"_couronnePelote|_haloPelote|_flaquePelote|(?:repeating-)?(?:radial|linear|conic)-gradient\(|create(?:Radial|Linear|Conic)Gradient|shadowBlur|shadowColor|drop-shadow\(|text-shadow\s*:[^;}\"']*|box-shadow\s*:[^;}\"']*")
LONG=r"-?\d*\.?\d+(?:px|em|rem)?"
def floue(val):
    """une ombre CSS n'est un VOLUME que si elle a un flou (3e longueur > 0) et n'est pas inset (un filet, pas un volume)"""
    for part in re.split(r",(?![^(]*\))", val.split(':',1)[1]):
        if 'inset' in part: continue
        n=re.findall(r"(-?\d*\.?\d+)(?:px|em|rem)?(?=\s|$|!)", part.replace('!important',' '))
        if len(n)>=3 and float(n[2])>0: return True
    return False
def blocs(S):
    return [(m.start(), m.group(1)) for m in re.finditer(r"<(?:style|script)[^>]*\bid=\"([^\"]+)\"", S)]
def occ(nom, S):
    B=blocs(S) if nom.endswith('.html') else []
    out=[]
    for m in MOTIFS.finditer(S):
        t=m.group(0)
        if t.startswith(('box-shadow','text-shadow')) and not floue(t): continue
        if t=='shadowColor': continue          # sans flou, une couleur d'ombre ne peint rien : shadowBlur la porte
        if t=='shadowBlur':
            fin=S[m.end():m.end()+12]
            if re.match(r"\s*=\s*0(?![.\d])", fin): continue   # remise à zéro
        lot='(hors bloc)'
        for p,i in B:
            if p<=m.start(): lot=i
            else: break
        ctx=re.sub(r"\s+"," ",S[max(0,m.start()-30):m.start()+40])
        out.append((nom, lot, ctx, t))
    return out
def balaye(moteur=None):
    A=io.open(os.path.join(ICI,'app.html'),encoding='utf-8').read()
    M=moteur if moteur is not None else io.open(os.path.join(ICI,'promi-moteur.js'),encoding='utf-8').read()
    return occ('app.html',A)+occ('promi-moteur.js',M)
def cle(o): return '%s | %s | %s'%o[:3]
def main():
    F=os.path.join(ICI,'volume-dette.json')
    moteur=None
    if any(a.startswith('--sonde') for a in sys.argv):
        M=io.open(os.path.join(ICI,'promi-moteur.js'),encoding='utf-8').read()
        old="g.fillStyle=bg;g.fillRect(0,0,W,H);"
        assert M.count(old)>=1, 'point de sonde absent'
        if '--sonde=mini' in sys.argv:
            moteur=M.replace(old, old+"try{ if(window._haloPelote) g.drawImage(window._haloPelote(120,40,44,8,[130,174,248],[5,3,2]),0,0); }catch(_){}",1)   # le mini halo sur une dalle
            print('SONDE : le MINI HALO de la Pelote (window._haloPelote) posé sur les dalles de la Toile, dans une copie du moteur')
        elif '--sonde=halo' in sys.argv:
            moteur=M.replace(old, old+"g.shadowBlur=14;g.shadowColor='rgba(130,174,248,.6)';",1)   # un halo sur les dalles de la Toile
            print('SONDE : un halo (shadowBlur 14) posé sur les dalles de la Toile, dans une copie du moteur')
        else:
            moteur=M.replace(old, old+"try{ if(window._couronnePelote) window._couronnePelote(g.canvas,[[130,174,248]],false); }catch(_){}",1)
            print('SONDE : une COURONNE (window._couronnePelote) posée sur les dalles de la Toile, dans une copie du moteur')
    O=balaye(moteur)
    if '--figer' in sys.argv:
        dette=[cle(o) for o in O if not permis(o[1],o[3])]
        json.dump(sorted(dette), open(F,'w',encoding='utf-8'), ensure_ascii=False, indent=0)
        print('dette figée :', len(dette), 'occurrences'); return
    dette=collections.Counter(json.load(open(F,encoding='utf-8')))
    vu=collections.Counter(); neuf=[]; blanche=0
    for o in O:
        if permis(o[1],o[3]): blanche+=1; continue
        k=cle(o)
        if vu[k]<dette[k]: vu[k]+=1
        else: neuf.append(k)
    print('liste blanche : l\'ombre de la Pelote seule (v139) —', blanche, 'occurrence(s) exemptée(s), attendu', OMBRE_ATTENDUE)
    if blanche!=OMBRE_ATTENDUE: neuf.append('(la liste blanche exempte %d occurrence(s) : l\'ombre en porte exactement %d)'%(blanche,OMBRE_ATTENDUE))
    print('dette de naissance :', sum(dette.values()), '· retrouvée :', sum(vu.values()), '· soldée depuis :', sum(dette.values())-sum(vu.values()))
    for k in neuf: print('  ✗ NOUVEAU VOLUME :', k)
    print(('✅ AUCUN VOLUME, NULLE PART — hors l’ombre de la Pelote' if not neuf else '❌ %d volume(s) nouveau(x)'%len(neuf)))
    sys.exit(1 if neuf else 0)
if __name__=='__main__': main()

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
Usage : python3 redteam_volume.py [--figer] [--sonde]
"""
import io, os, re, sys, json, collections
ICI=os.path.dirname(os.path.abspath(__file__))
# LISTE BLANCHE NOMINATIVE — (bloc → motifs permis). v115 : le halo flou devient la COURONNE de fibres ; son peintre,
# window._couronnePelote, est un VOLUME lui aussi : il n'est permis que dans son bloc et à son unique appel (l'Aura).
BLANCHE={'lot-V114-PELOTE-css':'*', 'lot-V115-PELOTE':'*', 'lot-AURA-PELOTE':{'_couronnePelote'}}
def permis(lot, motif):
    b=BLANCHE.get(lot); return b=='*' or (b is not None and any(motif.startswith(m) for m in b))
MOTIFS=re.compile(r"_couronnePelote|(?:repeating-)?(?:radial|linear|conic)-gradient\(|create(?:Radial|Linear|Conic)Gradient|shadowBlur|shadowColor|drop-shadow\(|text-shadow\s*:[^;}\"']*|box-shadow\s*:[^;}\"']*")
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
        if '--sonde=halo' in sys.argv:
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
    print('liste blanche (la Pelote) :', blanche, 'occurrence(s) dans', ', '.join(sorted(BLANCHE)))
    print('dette de naissance :', sum(dette.values()), '· retrouvée :', sum(vu.values()), '· soldée depuis :', sum(dette.values())-sum(vu.values()))
    if blanche==0: print('✗ la Pelote ne porte plus son halo ni son ombre'); neuf.append('(liste blanche vide)')
    for k in neuf: print('  ✗ NOUVEAU VOLUME :', k)
    print(('✅ AUCUN VOLUME HORS DE LA PELOTE' if not neuf else '❌ %d volume(s) hors de la Pelote'%len(neuf)))
    sys.exit(1 if neuf else 0)
if __name__=='__main__': main()

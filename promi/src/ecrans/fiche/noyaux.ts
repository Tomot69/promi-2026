/**
 * LES NOYAUX D'UNE FICHE (SPEC-ECRANS §4 ; le prototype : `openDetail` et `auraDisques` pour qui paraît, `karmaCircle` pour les comptes,
 * `noyaux()` de `_ficheCotes` et `drawKRing` pour l'anneau, lot-V181A-CERCLE pour le « + » orange, C-254) — « Toi » (78) puis les personnes
 * de la parole (58) : un anneau de deux arcs au plus, tenu `#00341A` puis en cours `#291547`, depuis midi, un jour de 3 pt d'arc entre eux
 * (C-210) ; un anneau vide porte la couleur de la nature et deux contours fins ; aucun filet (C-059). Le visage dedans, le prénom dessous.
 * Le « + » orange se pose 26 pt après le dernier petit disque, centré sur lui, sur une parole que je fais (jamais reçue).
 */
import type { Parole } from '../../donnees/schema.ts';
import { palette } from '../../design/jetons.ts';
import { avecAlpha, esc } from '../commun.ts';

export interface Noyau {
  nom: string;
  moi: boolean;
  tenues: number;
  enCours: number;
}

const champ = (p: Parole, k: string): unknown => (p as unknown as Record<string, unknown>)[k] ?? p.suite?.[k];

/**
 * qui paraît, dans l'ordre (`openDetail` du prototype) : « Toi », puis — un Chiche : ses personnes (`who`, puis `avec`) ; un Promi : `who` et
 * `from`, triés par ordre alphabétique (jamais par valeur). Un champ se coupe aux virgules et aux « · » ; « moi » et « le groupe » n'y sont
 * pas (à la casse près : « Moi » écrit par l'onboarding a son disque, comme dans le prototype). Une parole d'un Cercle : son disque de Cercle
 * (lot 5) — rien ici.
 */
export function noyauxDe(p: Parole, toutes: readonly Parole[]): Noyau[] {
  const miennes = toutes.filter((q) => !q.draft && (!q.from || q.from === 'moi'));
  const compte = (f: (q: Parole) => boolean): { tenues: number; enCours: number } => ({
    tenues: miennes.filter((q) => f(q) && q.status === 'tenu').length,
    enCours: miennes.filter((q) => f(q) && q.status === 'encours').length,
  });
  const out: Noyau[] = [{ nom: 'Toi', moi: true, ...compte(() => true) }];
  const un = (v: unknown): string[] =>
    (typeof v === 'string' ? v : '')
      .split(/\s*[,·]\s*/)
      .map((x) => x.trim())
      .filter((x) => x && x !== 'moi' && x !== 'le groupe');
  let noms: string[] = [];
  const ajoute = (x: string): void => {
    if (!noms.includes(x)) noms.push(x);
  };
  if (p.chiche) {
    un(p.who).forEach(ajoute);
    un(champ(p, 'avec')).forEach(ajoute);
  } else if (p.nuee && p.nuee !== 'soi') noms = [];
  else {
    un(p.who).forEach(ajoute);
    un(p.from).forEach(ajoute);
    noms.sort((a, b) => a.localeCompare(b));
  }
  for (const n of noms) out.push({ nom: n, moi: false, ...compte((q) => q.who === n) });
  return out;
}

const VISAGE = (d: number): string =>
  '<svg viewBox="0 0 ' +
  String(d) +
  ' ' +
  String(d) +
  '" aria-hidden="true"><circle cx="' +
  String(d / 2) +
  '" cy="' +
  (0.39 * d).toFixed(2) +
  '" r="' +
  (0.19 * d).toFixed(2) +
  '" fill="' +
  palette.creme95 +
  '"/><path d="M' +
  (0.2 * d).toFixed(2) +
  ' ' +
  (0.98 * d).toFixed(2) +
  ' A' +
  (0.3 * d).toFixed(2) +
  ' ' +
  (0.27 * d).toFixed(2) +
  ' 0 0 1 ' +
  (0.8 * d).toFixed(2) +
  ' ' +
  (0.98 * d).toFixed(2) +
  ' Z" fill="' +
  palette.creme95 +
  '"/></svg>';

/** la rangée (l'arbre du prototype : `.aura-track` › `.kring` › `.kr-wrap` [anneau, visage] + `.kr-n`) ; les canevas sont peints par `peindreNoyaux` */
export function rangeeNoyaux(N: Noyau[], natCol: string, tenue: boolean, court: (n: string) => string): string {
  return (
    '<div class="aura-track">' +
    N.map((n) => {
      const D = n.moi ? 78 : 58;
      const d = n.moi ? 48 : 36;
      const nom = n.moi
        ? 'Toi'
        : '<span class="nom-lien" data-nom="' + esc(n.nom) + '" role="link">' + esc(court(n.nom)) + '</span>';
      return (
        '<div class="kring' +
        (n.moi ? ' kring-moi' : '') +
        '"><span class="kr-wrap" style="width:' +
        String(D) +
        'px;height:' +
        String(D) +
        'px"><canvas class="kr-c" data-e="' +
        String(n.enCours) +
        '" data-t="' +
        String(n.tenues) +
        '" data-vide="' +
        natCol +
        '"></canvas><span class="s1b-visage" style="width:' +
        String(d) +
        'px;height:' +
        String(d) +
        'px;background:' +
        natCol +
        '">' +
        VISAGE(d) +
        '</span></span><div class="kr-n' +
        (tenue ? ' fi-sur-terre' : '') +
        '">' +
        nom +
        '</div></div>'
      );
    }).join('') +
    '</div>'
  );
}

/** le grain des anneaux (`_grain`, un motif de bruit 96 × 96, `soft-light`, 0,6) — le prototype le tire au hasard à chaque chargement ;
 * ici il est tiré d'une graine fixe (la même image d'une ouverture à l'autre) */
let bruit: HTMLCanvasElement | null = null;
function motifBruit(): HTMLCanvasElement {
  if (bruit) return bruit;
  const c = document.createElement('canvas');
  c.width = c.height = 96;
  const g = c.getContext('2d')!;
  const im = g.createImageData(96, 96);
  let s = 0x9e3779b9;
  const r = (): number => {
    s ^= s << 13;
    s ^= s >>> 17;
    s ^= s << 5;
    return (s >>> 0) / 4294967296;
  };
  for (let i = 0; i < im.data.length; i += 4) {
    const v = 140 + r() * 115;
    im.data[i] = im.data[i + 1] = im.data[i + 2] = v;
    im.data[i + 3] = r() * 24;
  }
  g.putImageData(im, 0, 0);
  bruit = c;
  return c;
}

/** peint chaque anneau à la densité de l'écran (le prototype : D × 3) */
export function peindreNoyaux(hote: HTMLElement): void {
  for (const cv of hote.querySelectorAll<HTMLCanvasElement>('canvas.kr-c')) {
    const D = parseFloat(cv.parentElement!.style.width);
    const EP = D === 78 ? 12 : 9;
    const k = 3;
    cv.width = cv.height = Math.round(D * k);
    cv.style.width = cv.style.height = `${String(D)}px`;
    const g = cv.getContext('2d');
    if (!g) continue;
    const Wc = cv.width;
    const c = Wc / 2;
    const R = ((D - EP) / 2 / D) * Wc;
    const lw = (EP / D) * Wc;
    g.clearRect(0, 0, Wc, Wc);
    const e = +(cv.dataset['e'] ?? 0);
    const t = +(cv.dataset['t'] ?? 0);
    const tot = e + t;
    g.lineCap = 'butt';
    g.lineWidth = lw;
    if (!tot) {
      g.strokeStyle = cv.dataset['vide'] ?? palette.bleu45;
      g.beginPath();
      g.arc(c, c, R, 0, Math.PI * 2);
      g.stroke();
      g.strokeStyle = avecAlpha(palette.creme92, 0.9);
      g.lineWidth = Math.max(2.5, lw * 0.16);
      for (const rr of [R - lw / 2 + g.lineWidth / 2, R + lw / 2 - g.lineWidth / 2]) {
        g.beginPath();
        g.arc(c, c, rr, 0, Math.PI * 2);
        g.stroke();
      }
      continue;
    }
    const parts = (
      [
        [t, palette.menthe11],
        [e, palette.mauve12],
      ] as Array<[number, string]>
    ).filter((x) => x[0] > 0);
    const GJ = parts.length > 1 ? (3 * k) / R : 0;
    let a = -Math.PI / 2;
    for (const [n, col] of parts) {
      const L = (n / tot) * Math.PI * 2;
      g.strokeStyle = col;
      g.beginPath();
      if (parts.length > 1) g.arc(c, c, R, a + GJ / 2, a + L - GJ / 2);
      else g.arc(c, c, R, 0, Math.PI * 2);
      g.stroke();
      a += L;
    }
    // le grain, dans la bande de l'anneau seulement
    g.save();
    g.beginPath();
    g.arc(c, c, R + lw / 2, 0, Math.PI * 2);
    g.arc(c, c, R - lw / 2, 0, Math.PI * 2, true);
    g.clip();
    const pat = g.createPattern(motifBruit(), 'repeat');
    if (pat) {
      pat.setTransform(new DOMMatrix([88 / 96, 0, 0, 88 / 96, 0, 0]));
      g.globalCompositeOperation = 'soft-light';
      g.globalAlpha = 0.6;
      g.fillStyle = pat;
      g.fillRect(0, 0, Wc, Wc);
    }
    g.restore();
  }
}

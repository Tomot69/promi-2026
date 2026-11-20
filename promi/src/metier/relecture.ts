/**
 * LES PASSES DE RELECTURE — ce que le prototype applique à son état relu (`loadState`), réécrit en fonctions pures.
 * Elles sont idempotentes : appliquées une fois à l'import, elles ne changent plus rien ensuite.
 *  · `sansTombes`     une parole effacée ne revient jamais (v187 : `id|titre` dans `effacees`) ;
 *  · `reparerPlaces`  v160 (C-177) : une place invalide est effacée ; deux places à moins de 0,003 l'une de l'autre dans la même famille de
 *                     semis : la plus ancienne parole garde la sienne (le moteur choisira une cellule pour l'autre) ; les Cercles aussi ;
 *  · `figerDalles`    13 sept. (Q213) : une parole sans couleur figée la reçoit de son titre et de sa personne (FNV-1a), jamais de son id ;
 *  · `poserCles`      v203 (Q621, `lot-V203-CLE`) : une parole plantée sans clé de plantation reçoit son titre (le moteur lit `cle` à la place du
 *                     titre pour tirer sa dalle) ; un gardé de côté n'en a pas.
 */
import type { CouleurDalle, Parole, Place } from '../donnees/schema.ts';

export function tombe(p: Pick<Parole, 'id' | 'title'>): string {
  return p.id + '|' + (p.title || '');
}

export function sansTombes(paroles: Parole[], effacees: string[]): Parole[] {
  if (!effacees.length) return paroles;
  const t = new Set(effacees);
  return paroles.filter((p) => !t.has(tombe(p)));
}

export function placeValide(v: unknown): v is Place {
  if (!Array.isArray(v) || v.length < 2 || v.length > 3) return false;
  const [x, y, f] = v as unknown[];
  if (typeof x !== 'number' || typeof y !== 'number' || !isFinite(x) || !isFinite(y)) return false;
  if (x < 0 || x > 1 || y < 0 || y > 1 || (x === 0 && y === 0)) return false;
  return v.length < 3 || f === 0 || f === 1;
}

export function reparerPlaces(
  paroles: Parole[],
  cercles: Record<string, Place>,
): { paroles: Parole[]; cercles: Record<string, Place>; effacees: number } {
  const vues: Place[] = [];
  let n = 0;
  const proche = (v: Place): boolean =>
    vues.some((u) => (u[2] ?? 0) === (v[2] ?? 0) && Math.abs(u[0] - v[0]) < 0.003 && Math.abs(u[1] - v[1]) < 0.003);
  const parId = new Map<number, Parole>();
  for (const p of [...paroles].sort((a, b) => (a.id || 0) - (b.id || 0))) {
    if (p.place == null) continue;
    if (!placeValide(p.place)) {
      const q = { ...p };
      delete q.place;
      parId.set(p.id, q);
      n++;
      continue;
    }
    if (p.draft) continue;
    if (proche(p.place)) {
      const q = { ...p };
      delete q.place;
      parId.set(p.id, q);
      n++;
      continue;
    }
    vues.push(p.place);
  }
  const C: Record<string, Place> = {};
  for (const k of Object.keys(cercles).sort()) {
    const v = cercles[k];
    if (!placeValide(v) || proche(v)) {
      n++;
      continue;
    }
    C[k] = v;
    vues.push(v);
  }
  return { paroles: paroles.map((p) => parId.get(p.id) ?? p), cercles: C, effacees: n };
}

export function dalleDeCle(p: Pick<Parole, 'title' | 'who'>): CouleurDalle {
  const s = String(p.title || '') + '|' + String(p.who || '');
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619) >>> 0;
  }
  return { ci: h % 4, lit: 0 };
}

export function figerDalles(paroles: Parole[]): Parole[] {
  return paroles.map((p) => (p.dalle ? p : { ...p, dalle: dalleDeCle(p) }));
}

export function poserCles(paroles: Parole[]): Parole[] {
  return paroles.map((p) => {
    if (p.cle != null || p.draft || p.suite?.['brouillon'] || p.title == null) return p;
    return { ...p, cle: String(p.title) };
  });
}

/**
 * L'ÉCHÉANCE EST UNE DATE (v151, C-160, `lot-V151-ECHEANCE`) : `ech = {iso, due}` ; `due` (les jours qui restent) n'en est que la
 * conséquence, recomptée contre AUJOURD'HUI au lancement et à chaque retour au premier plan. Réécrit de `note` et `recompte`, à l'identique :
 * une date choisie au calendrier (`dueISO`) EST l'échéance ; un `due` changé sans date (REPORTER, « 5 jours ») pose la date ; sans
 * `due`, plus de date. `aujourdhui` : minuit local.
 */
function isoDe(d: Date): string {
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}
function dateDe(s: unknown): Date | null {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(typeof s === 'string' ? s : '');
  return m ? new Date(+m[1]!, +m[2]! - 1, +m[3]!) : null;
}
export function minuit(maintenant: Date = new Date()): Date {
  const d = new Date(maintenant);
  d.setHours(0, 0, 0, 0);
  return d;
}

export function recompterEcheances(paroles: Parole[], aujourdhui: Date): Parole[] {
  const ecart = (d: Date): number => Math.round((d.getTime() - aujourdhui.getTime()) / 864e5);
  return paroles.map((p0) => {
    if (p0.draft) return p0;
    const p: Parole = { ...p0 };
    const s = p.suite ? { ...p.suite } : undefined;
    const dueISO = s?.['dueISO'];
    // note(p)
    let note = true;
    if (dueISO && (!p.ech || p.ech.iso !== dueISO)) {
      const dq = dateDe(dueISO);
      if (dq) {
        p.ech = { iso: dueISO as string, due: ecart(dq) };
        p.due = p.ech.due;
        note = false;
      }
    }
    if (note && !(p.ech && p.ech.due === p.due)) {
      if (p.due === undefined || p.due === null || isNaN(+p.due)) {
        if (s && p.ech && s['dueISO'] === p.ech.iso) delete s['dueISO'];
        delete p.ech;
      } else {
        const d = new Date(aujourdhui);
        d.setDate(d.getDate() + Math.round(+p.due));
        if (s && p.ech && s['dueISO'] === p.ech.iso) delete s['dueISO'];
        p.ech = { iso: isoDe(d), due: Math.round(+p.due) };
        p.due = p.ech.due;
      }
    }
    // recompte
    if (p.ech) {
      const d = dateDe(p.ech.iso);
      if (d) {
        const j = ecart(d);
        p.due = j;
        p.ech = { ...p.ech, due: j };
      }
    }
    if (s) p.suite = s;
    return p;
  });
}

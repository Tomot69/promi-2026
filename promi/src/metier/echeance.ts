/**
 * L'ÉCHÉANCE, SES MOTS (le prototype : `_dateQuand`, et le mot de « AVANT » d'une fiche, `#dDue` — v16, v151 C-160).
 * Partagés par la page + (le choix d'une date) et le Peaufiner d'une fiche (la rangée AVANT).
 */
import type { Parole } from '../donnees/schema.ts';

const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
const MOIS = [
  'janvier',
  'février',
  'mars',
  'avril',
  'mai',
  'juin',
  'juillet',
  'août',
  'septembre',
  'octobre',
  'novembre',
  'décembre',
];

/** « lundi 12 » ; au-delà de 30 jours, le mois (« lundi 12 mai ») ; jamais l'année */
export function dateQuand(d: Date, jours: number): string {
  const base = `${JOURS[d.getDay()]!} ${String(d.getDate())}`;
  return jours > 30 ? `${base} ${MOIS[d.getMonth()]!}` : base;
}

function dateIso(s: unknown): Date | null {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(typeof s === 'string' ? s : '');
  return m ? new Date(+m[1]!, +m[2]! - 1, +m[3]!) : null;
}

/**
 * le mot de la rangée AVANT d'une fiche (le texte de `#dDue` sans « avant ») : « en l’air » pour une envie (`enLair`) ; la date choisie au
 * calendrier ; « un jour » sans échéance ; sinon la date de l'échéance
 */
export function motAvant(p: Parole, aujourdhui: Date): string {
  const s = p.suite ?? {};
  if (s['enLair']) return 'en l’air';
  const jours = (d: Date): number => Math.round((d.getTime() - aujourdhui.getTime()) / 864e5);
  const iso = dateIso(s['dueISO']);
  if (iso) return dateQuand(iso, jours(iso));
  if (p.due == null || Number.isNaN(+p.due)) return 'un jour';
  const d = dateIso(p.ech?.iso) ?? new Date(aujourdhui.getTime() + Math.round(+p.due) * 864e5);
  return dateQuand(d, jours(d));
}

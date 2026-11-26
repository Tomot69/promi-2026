/**
 * L0 §2 — L'IMPORT DES DONNÉES DE TOM, SANS AUCUNE PERTE : pour chaque export (etats/ de Tom, le dossier de référence, banc-etats/),
 * l'import puis le retour au format du prototype redonnent le stockage d'origine (chaque clé ; `promi_state` et `promi_studio` comparés
 * une fois relus, l'ordre des clés d'un objet n'étant pas une donnée). Seules exceptions, nommées : la clé `setItem` (le texte d'une fonction,
 * pas une donnée) et `status: 'rate'` → `'encours'` (C-210, la relecture du prototype lui-même).
 */
import { describe, expect, it } from 'vitest';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { importer, versPrototype, stockageDe } from '../../src/donnees/migrations/prototype.ts';
import { migrer } from '../../src/donnees/migrations/index.ts';

const RACINE = join(import.meta.dirname, '..', '..', '..');
const DOSSIERS = [
  join(RACINE, 'etats'),
  join(RACINE, '..', '..', 'Promi-reference-v205', 'etat-de-tom'),
  join(RACINE, 'banc-etats'),
];
const EXPORTS = DOSSIERS.filter(existsSync).flatMap((d) =>
  readdirSync(d)
    .filter((f) => f.endsWith('.json'))
    .map((f) => join(d, f)),
);

function relu(k: string, v: string): unknown {
  if (k === 'promi_state') {
    const st = JSON.parse(v) as { promises: Array<Record<string, unknown>> };
    for (const p of st.promises) if (p['status'] === 'rate') p['status'] = 'encours';
    return st;
  }
  try {
    return JSON.parse(v) as unknown;
  } catch {
    return v;
  }
}

describe("l'import de l'export du prototype", () => {
  it('trouve des exports à juger', () => expect(EXPORTS.length).toBeGreaterThanOrEqual(5));
  for (const f of EXPORTS)
    it(`sans perte : ${f.slice(RACINE.length - 20)}`, () => {
      const x = JSON.parse(readFileSync(f, 'utf8')) as Record<string, unknown>;
      const ls = stockageDe(x as never);
      const retour = versPrototype(importer(x as never));
      const attendu: Record<string, unknown> = {};
      for (const [k, v] of Object.entries(ls)) if (k !== 'setItem') attendu[k] = relu(k, v);
      const obtenu: Record<string, unknown> = {};
      for (const [k, v] of Object.entries(retour)) obtenu[k] = relu(k, v);
      expect(obtenu).toEqual(attendu);
    });
  it("l'état de Tom du 17 nov. : sa parole, son prénom, sa graine, son monde", () => {
    const f = EXPORTS.find((x) => x.endsWith('tom-20261117-211127.json'));
    if (!f) return;
    const e = migrer(JSON.parse(readFileSync(f, 'utf8')));
    expect(e.schema).toBe(3);
    expect(e.infosCercles).toEqual({});
    expect(e.paroles.map((p) => [p.id, p.title, p.status])).toEqual([[125, 'Test', 'tenu']]);
    expect(e.utilisateur).toEqual({ prenom: 'Tom', graine: 936256980 });
    expect(e.studio.monde).toBe('encre');
    expect(e.paroles[0]!.comments?.[0]?.t).toBe('Dddd');
  });
});

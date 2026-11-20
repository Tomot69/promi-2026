/** Les pièces reprises (le moteur, le tracé, les flaques) sont des copies OCTET POUR OCTET du prototype : on ne les corrige jamais ici. */
import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const SRC = join(import.meta.dirname, '..', '..', 'src');
const RACINE = join(import.meta.dirname, '..', '..', '..');
const man = JSON.parse(readFileSync(join(SRC, 'repris.json'), 'utf8')) as Record<
  string,
  { source: string; sha256: string }
>;
const sha = (f: string): string => createHash('sha256').update(readFileSync(f)).digest('hex');

describe('les pièces reprises du prototype', () => {
  for (const [copie, { source, sha256 }] of Object.entries(man)) {
    it(`${copie} = ${source}, octet pour octet`, () => {
      expect(sha(join(SRC, copie))).toBe(sha256);
      if (existsSync(join(RACINE, source))) expect(sha(join(RACINE, source))).toBe(sha256);
    });
  }
});

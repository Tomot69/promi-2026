/**
 * LA MIGRATION 1 → 2 (lot 2a) : le gardé de côté (`draft`) porte l'état de la page + qui l'a gardé, `brouillon`, un champ que le schéma v1
 * rangeait dans `suite` (un champ du prototype pas encore nommé). Il passe à sa place ; rien d'autre ne change, rien ne se perd.
 */
type Brut = Record<string, unknown>;

export function migrer1vers2(e: { schema: number } & Brut): { schema: number } & Brut {
  const paroles = Array.isArray(e['paroles']) ? (e['paroles'] as Brut[]) : [];
  return {
    ...e,
    schema: 2,
    paroles: paroles.map((p) => {
      const suite = p['suite'] as Brut | undefined;
      if (!suite || !('brouillon' in suite)) return p;
      const { brouillon, ...reste } = suite;
      const q: Brut = { ...p, brouillon };
      if (Object.keys(reste).length) q['suite'] = reste;
      else delete q['suite'];
      return q;
    }),
  };
}

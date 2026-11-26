/**
 * LA MIGRATION 2 → 3 (lot 5) : les réglages d'un Cercle que Peaufiner écrit — sa DESCRIPTION, ses PIÈCES JOINTES, son TRAIT (`infosCercles`).
 * Le prototype les gardait en mémoire seulement (`NUENOTE`, `NUEFILES`, `NUEE` : perdus au rechargement) ; la vraie app les garde. Un état v2
 * n'en a aucun : la table naît vide. Rien d'autre ne change, rien ne se perd.
 */
type Brut = Record<string, unknown>;

export function migrer2vers3(e: { schema: number } & Brut): { schema: number } & Brut {
  return { ...e, schema: 3, infosCercles: {} };
}

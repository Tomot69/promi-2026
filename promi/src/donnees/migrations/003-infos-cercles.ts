/**
 * LA MIGRATION 2 → 3 (lot 5) : ce qu'un Cercle porte en propre (`infosCercles`) — sa DESCRIPTION, ses PIÈCES JOINTES, son TRAIT, que Peaufiner
 * écrit, et SES MOTS. Le prototype gardait les trois premiers en mémoire seulement (`NUENOTE`, `NUEFILES`, `NUEE` : perdus au rechargement) ; les
 * mots, dans une clé de l'appareil (`promi_cercle_mots`, gardée telle quelle dans `autres` jusqu'ici) : ils passent à leur place, la clé part.
 * Rien d'autre ne change, rien ne se perd (une clé illisible reste dans `autres`). L'import d'un export du prototype les range de même.
 */
type Brut = Record<string, unknown>;

/** les mots des Cercles sortis de la clé de l'appareil (`promi_cercle_mots`) : la table neuve, et `autres` sans la clé (illisible : gardée) */
export function rangerMotsCercles(autres0: Readonly<Record<string, string>>): {
  infos: Record<string, { mots: unknown[] }>;
  autres: Record<string, string>;
} {
  const autres = { ...autres0 };
  const infos: Record<string, { mots: unknown[] }> = {};
  const brut = autres['promi_cercle_mots'];
  if (brut != null)
    try {
      const M = JSON.parse(brut) as Record<string, unknown>;
      for (const [k, l] of Object.entries(M)) if (Array.isArray(l) && l.length) infos[k] = { mots: l };
      delete autres['promi_cercle_mots'];
    } catch {
      /* illisible : gardé tel quel */
    }
  return { infos, autres };
}

export function migrer2vers3(e: { schema: number } & Brut): { schema: number } & Brut {
  const { infos, autres } = rangerMotsCercles((e['autres'] as Record<string, string> | undefined) ?? {});
  return { ...e, schema: 3, infosCercles: infos, autres };
}

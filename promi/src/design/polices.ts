/**
 * Les cinq faces (CLAUDE.md §6), chargées AVANT le premier écran : la Toile écrit ses titres sur un canevas, et un canevas ne demande
 * pas une police au navigateur — sans ce chargement, le premier titre sortait dans la police de secours (mesuré au banc : 805 px
 * d'écart sur « MOI · Test »).
 */
export const FACES = [
  '700 16px Gilbert',
  '400 16px Atkinson',
  '500 16px Atkinson',
  '700 16px Atkinson',
  '400 16px PromiLate',
] as const;

export async function chargerPolices(): Promise<void> {
  const chargees = await Promise.all(FACES.map((f) => document.fonts.load(f)));
  await document.fonts.ready;
  // une face qui ne se charge pas ne doit jamais passer en silence (vécu en L0 : un `src` mal écrit, la Toile en police de secours)
  const manquantes = FACES.filter((_, i) => !chargees[i]?.length);
  if (manquantes.length) throw new Error('polices non chargées : ' + manquantes.join(', '));
}

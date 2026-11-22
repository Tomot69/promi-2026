/**
 * PAS D'EMOJI DANS PROMI (C-129, v146 — `lot-V146-EMOJI` du prototype) : « un emoji tapé ou collé n'est tout simplement pas inséré : rien ne
 * s'affiche, aucun message ». Filtrés : les pictogrammes étendus, les sélecteurs de variante (FE0E, FE0F), la jonction (200D), les teintes de
 * peau, les drapeaux (indicateurs régionaux, étiquettes E0020–E007F) et les touches numérotées (chiffre, # ou * suivi de FE0F 20E3 : la touche
 * entière part, chiffre compris). Le texte autour reste.
 */
const TOUCHE = /[0-9#*]️?⃣/gu;
const RX =
  /[\p{Extended_Pictographic}\p{Emoji_Modifier}\p{Regional_Indicator}\u{E0020}-\u{E007F}]|\u200D|\uFE0E|\uFE0F|\u20E3/gu;

export function sansEmoji(s: string): string {
  return s ? s.replace(TOUCHE, '').replace(RX, '') : s;
}

/** un champ qui ne laisse entrer aucun emoji : à l'entrée (`beforeinput`), au collage, et après coup (`input`, le curseur à sa place) */
export function champSansEmoji(c: HTMLInputElement | HTMLTextAreaElement): void {
  const insere = (d: string): void => {
    const a = c.selectionStart ?? c.value.length;
    const b = c.selectionEnd ?? a;
    c.setRangeText(d, a, b, 'end');
    c.dispatchEvent(new Event('input', { bubbles: true }));
  };
  c.addEventListener('beforeinput', (ev) => {
    const e = ev as InputEvent;
    if (e.data == null) return;
    const d = sansEmoji(e.data);
    if (d === e.data) return;
    e.preventDefault();
    if (d) insere(d);
  });
  c.addEventListener('paste', (ev) => {
    const e = ev as ClipboardEvent;
    const x = e.clipboardData?.getData('text') ?? '';
    const d = sansEmoji(x);
    if (d === x) return;
    e.preventDefault();
    if (d) insere(d);
  });
  c.addEventListener(
    'input',
    () => {
      const v = c.value;
      const w = sansEmoji(v);
      if (w === v) return;
      const avant = sansEmoji(v.slice(0, c.selectionStart ?? v.length));
      c.value = w;
      c.setSelectionRange(avant.length, avant.length);
    },
    true,
  );
}

/**
 * LOT 3a-1 — LA FICHE AU REPOS : IDENTITÉ AU PIXEL (releve-S1-fiches, redteam_fiches_theme, redteam_fiches_orange, redteam_deux_etats,
 * redteam_phrase_fiche, redteam_motmarque, redteam_etat_fiche, redteam_formes, redteam_champ, redteam_contraste_trait, redteam_ronds).
 *
 * La fiche de la vraie app à 390 × 844 contre celle du prototype (son appareil dans la fenêtre du banc), le même état des deux côtés
 * (`banc-etats/etat-fiches.json` : un cas par état de fiche), même WebKit, ×3, clair et sombre (C-132 : la même fiche), échelles 1 et 0,79 :
 * Promi en cours à soi, à Marion, à cinq personnes, date passée (« EN COURS · 12 OCT. »), reçue ; tenue ; Chiche lancé à soi, à Adrien,
 * à Rachel et Marion avec une part tracée (C-115), reçu à relever (D2), tenu, tenu à deux. La fiche est ouverte par la façade de chaque côté
 * (`openDetail(id)` ; `fiche().ouvrir(id)`), les animations gelées. Tolérance : 2 niveaux, 0 pixel au-delà (Q616 hors du Mac, aides.ts `ecart`).
 *
 * EXCEPTIONS NOMMÉES (et seulement elles), masquées des deux côtés :
 *  · M1 — la MATIÈRE de la dalle (§8 bis : « zéro écart » excepte la matière) : la boîte que le peintre déclare (`data-matiere`), + 8 pt ;
 *  · M2 — le GRAIN des anneaux des Noyaux (`_grain`) : le prototype le tire au hasard à chaque chargement (`Math.random`), la vraie app d'une
 *         graine fixe ; la bande de chaque anneau est masquée, ses arcs (couleurs, parts, jour de 3 pt) jugés à part (`fiche-juges.spec.ts`).
 *  · M3 — le FONDU à droite de la rangée des Noyaux quand elle déborde (plus de trois personnes) : un dégradé en masque d'août (`.aura-band`),
 *         une dette du volume du prototype (volume-dette.json) que la vraie app ne reprend pas — sa rangée s'arrête net ; ses 46 derniers pt
 *         sont masqués, et seulement quand elle déborde.
 */
import { test, expect } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import {
  fichesPilotees,
  images,
  ecart,
  sonde,
  stockageFiches,
  CAS_FICHES,
  zonesFiche,
  masquerFiche,
  type Zone,
} from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'fiche');
for (const theme of ['sombre', 'clair'] as const)
  for (const [id, cas] of CAS_FICHES)
    test(`identité au pixel : la fiche — ${cas}, ${theme}`, async ({ browser }) => {
      const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const { P, A, erreurs } = await fichesPilotees(browser, ls, id);
      try {
        // la sonde (sur « identité au pixel : la fiche — Promi en cours, à soi, sombre ») : le titre de la vraie app décalé d'un point
        if (sonde('fiche-identite-decale'))
          await A.addStyleTag({ content: '#detailPoster.fiche .fi-titre{translate:0 1px!important}' });
        const dv = await P.evaluate(() => {
          const r = document.getElementById('device')!.getBoundingClientRect();
          return { x: r.left, y: r.top, width: r.width, height: r.height };
        });
        // les deux côtés POSÉS : deux images identiques (matière exceptée) à 40 images d'horloge d'écart
        let Z: Zone[] = [];
        let n = 0;
        let ip: Buffer = Buffer.alloc(0);
        let ia: Buffer = Buffer.alloc(0);
        for (let k = 0; k < 20; k++) {
          await Promise.all([images(P, 40), images(A, 40)]);
          const Z2 = await zonesFiche(A, P);
          const n2 = await A.evaluate(() => document.querySelectorAll('#detailPoster.fiche canvas.kr-c').length);
          const ip2 = masquerFiche(await P.screenshot({ clip: dv }), Z2, n2);
          const ia2 = masquerFiche(await A.screenshot(), Z2, n2);
          // le X du prototype passe parfois, à l'ouverture d'une fiche tenue, par une place transitoire (sur le « P » de PROMI : la veille
          // de `lot-V157-CROIX` qui le repose) — on attend qu'il soit à SA place (x 300 ± 0,5) avant de comparer
          const xEnPlace = await P.evaluate(() => {
            const D = document.getElementById('device')!.getBoundingClientRect();
            const x = document.querySelector('#detailPoster .closeb')?.getBoundingClientRect();
            return !!x && Math.abs((x.left - D.left) / (D.width / 390) - 300) < 0.5;
          });
          // et l'encre du plateau du prototype posée (sur une machine lente, PROMI et le X sont un moment à l'encre noire : une passe de sa
          // composition qui n'est pas finie)
          const encre = (pg: typeof P): Promise<string> =>
            pg.evaluate(() => getComputedStyle(document.getElementById('dptNat')!).webkitTextFillColor);
          const encrePosee = (await encre(P)) === (await encre(A));
          const pose = k > 1 && xEnPlace && encrePosee && ip2.equals(ip) && ia2.equals(ia);
          [Z, n, ip, ia] = [Z2, n2, ip2, ia2];
          if (pose) break;
        }
        void n;
        mkdirSync(RES, { recursive: true });
        writeFileSync(join(RES, `${theme}-${String(id)}-prototype.png`), ip);
        writeFileSync(join(RES, `${theme}-${String(id)}-app.png`), ia);
        const e = ecart(ip, ia);
        expect(erreurs).toEqual([]);
        expect(
          { n: e.n, boite: e.boite },
          `pixels écartés de plus de 2 niveaux (zones exceptées ${JSON.stringify(Z)} ; bords lissés hors macOS : ${String(e.bords)})`,
        ).toEqual({ n: 0, boite: null });
      } finally {
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });

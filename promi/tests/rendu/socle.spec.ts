/**
 * L0 §2 — LE SOCLE DANS LE NAVIGATEUR DE L'iPHONE (WebKit) : les cinq faces chargées ; le tracé des lettres et les flaques chargés par leur
 * interface et menés par l'HORLOGE UNIQUE (en mode piloté, rien n'avance tant qu'on ne donne pas d'images) ; aucune erreur.
 */
import { test, expect } from '@playwright/test';
import { T_FIGE } from './banc.ts';

test('le socle : polices, tracé et flaques derrière leurs interfaces, menés par la seule horloge', async ({ page }) => {
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));
  await page.goto(`http://127.0.0.1:5180/?banc=1&pilote=${T_FIGE}`);
  await page.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
  const r = await page.evaluate(async () => {
    type P = {
      demarrer(o?: { accueil?: boolean }): Promise<void>;
      horloge: { images(n: number): void; maintenant(): number };
      chargerTrace(): {
        trace(el: HTMLElement, c: null, o?: object): { etat(): { texteReel: number; total: number; t: number } };
      };
      chargerFlaques(): { alea(g: number): () => number; Scene: unknown };
    };
    const p = (window as unknown as { __promi: P }).__promi;
    await p.demarrer({ accueil: false });
    const faces = [
      '700 16px Gilbert',
      '400 16px Atkinson',
      '500 16px Atkinson',
      '700 16px Atkinson',
      '400 16px PromiLate',
    ].map((f) => document.fonts.check(f));
    const T = p.chargerTrace();
    const F = p.chargerFlaques();
    const el = document.createElement('div');
    el.style.cssText = 'position:fixed;left:20px;top:300px;font:500 25px Atkinson;color:#201908';
    el.id = 'essaiTrace';
    el.textContent = 'Toi, c’est … ?';
    document.body.appendChild(el);
    const c = T.trace(el, null, {});
    (window as unknown as { __c: unknown }).__c = c;
    return { faces, flaques: typeof F.alea(7)() === 'number' && typeof F.Scene === 'function', avant: c.etat() };
  });
  // le tracé prépare ses lettres dans un ouvrier (un Worker : du vrai temps) ; ses images, elles, ne passent que si l'horloge en donne
  const t0 = (await page.evaluate('window.__promi.horloge.maintenant()')) as number;
  let apres = r.avant;
  for (let i = 0; i < 300 && !(apres.total > 0 && apres.texteReel >= apres.total); i++) {
    await page.waitForTimeout(20);
    apres = (await page.evaluate('(window.__promi.horloge.images(3), window.__c.etat())')) as typeof apres;
  }
  const t1 = (await page.evaluate('window.__promi.horloge.maintenant()')) as number;
  const texte = await page.evaluate("document.getElementById('essaiTrace').textContent");
  expect(erreurs).toEqual([]);
  expect(r.faces).toEqual([true, true, true, true, true]);
  expect(apres.total).toBeGreaterThan(0);
  expect(apres.texteReel, 'le tracé finit, mené par les images de l’horloge').toBe(apres.total);
  expect(t1 - t0, 'le temps n’avance que par les images données').toBeCloseTo(
    Math.round((t1 - t0) / (1000 / 60)) * (1000 / 60),
    3,
  );
  expect(texte).toBe('Toi, c’est … ?');
  expect(r.flaques).toBe(true);
});

/**
 * LES SONDES (C-326, Tom, 20 nov. 2026 : « chaque test rougit sur une sonde ») — un test qui ne prend pas la version fautive ne vaut rien
 * (CLAUDE.md §7). Chaque sonde est inscrite dans `tests/rendu/sondes/<fichier>.json` : `[{ "nom", "test", "defaut" }]` — le nom que le test
 * lit (`sonde('nom')`, tests/rendu/aides.ts), le titre exact du test, et le défaut qu'elle pose, en une phrase. Cet outil rejoue chaque test
 * avec sa sonde (`PROMI_SONDE=nom`) et exige qu'il ROUGISSE ; il vérifie aussi que chaque `sonde('…')` des tests est inscrite, et
 * l'inverse. Une sonde que son test ne prend pas : l'outil échoue, et le test est mort.
 * Une sonde est prise au PREMIER test qui rougit (`--max-failures=1`) : une sonde qui vise une famille de tests (les huit identités de la
 * page +) ne les rejoue pas tous en échec — `pp-identite-decale` a pris 41 min ainsi et fait dépasser l'heure à sa part (CI du 23 nov.).
 *   node outils/sondes.ts                 toutes les sondes (l'app construite, `vite preview` sur 5180)
 *   node outils/sondes.ts <nom> [<nom>…]  celles-là seulement
 *   node outils/sondes.ts --part=2/4      la deuxième des quatre parts (l'intégration continue)
 */
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const ICI = import.meta.dirname;
const DOSSIER = join(ICI, '..', 'tests', 'rendu');
type Sonde = { nom: string; test: string; defaut: string; fichier: string };

const sondes: Sonde[] = [];
for (const f of readdirSync(join(DOSSIER, 'sondes')).filter((x) => x.endsWith('.json'))) {
  const fichier = f.replace(/\.json$/, '.spec.ts');
  for (const s of JSON.parse(readFileSync(join(DOSSIER, 'sondes', f), 'utf8')) as Omit<Sonde, 'fichier'>[])
    sondes.push({ ...s, fichier });
}

// chaque sonde lue par un test est inscrite, et chaque sonde inscrite est lue par le test qu'elle nomme
const lues = new Map<string, string>();
for (const f of readdirSync(DOSSIER).filter((x) => x.endsWith('.spec.ts')))
  for (const m of readFileSync(join(DOSSIER, f), 'utf8').matchAll(/\bsonde\(\s*'([^']+)'\s*\)/g)) lues.set(m[1]!, f);
const fautes: string[] = [];
const noms = new Set<string>();
for (const s of sondes) {
  if (noms.has(s.nom)) fautes.push(`sonde inscrite deux fois : ${s.nom}`);
  noms.add(s.nom);
  if (lues.get(s.nom) !== s.fichier) fautes.push(`sonde inscrite mais lue par aucun test de ${s.fichier} : ${s.nom}`);
  if (!readFileSync(join(DOSSIER, s.fichier), 'utf8').includes(s.test.slice(0, 40)))
    fautes.push(`le test de la sonde ${s.nom} n'est pas dans ${s.fichier} : « ${s.test} »`);
}
for (const [n, f] of lues) if (!noms.has(n)) fautes.push(`sonde lue par ${f} mais pas inscrite : ${n}`);

// `--part=i/n` : la i-ième des n parts (l'intégration continue les passe en parallèle) ; les noms donnés : celles-là seulement
const part = /^--part=(\d+)\/(\d+)$/.exec(process.argv.find((a) => a.startsWith('--part=')) ?? '');
const seules = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const choix = (seules.length ? sondes.filter((s) => seules.includes(s.nom)) : sondes).filter(
  (_, k) => !part || k % +part[2]! === +part[1]! - 1,
);
const echappe = (t: string): string => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const lignes: string[] = [];
let ratees = 0;
for (const s of choix) {
  const t0 = Date.now();
  const r = spawnSync(
    'npx',
    [
      'playwright',
      'test',
      s.fichier,
      '-g',
      echappe(s.test),
      '--workers=1',
      '--retries=0',
      '--max-failures=1',
      '--reporter=line',
    ],
    { cwd: join(ICI, '..'), env: { ...process.env, PROMI_SONDE: s.nom }, encoding: 'utf8' },
  );
  const sortie = (r.stdout ?? '') + (r.stderr ?? '');
  const aucun = /No tests found|0 passed/.test(sortie) && !/failed/.test(sortie);
  const prise = r.status !== 0 && !aucun;
  if (!prise) ratees++;
  lignes.push(
    `${prise ? 'PRISE ' : 'RATÉE '} ${s.nom.padEnd(28)} ${((Date.now() - t0) / 1000).toFixed(0).padStart(4)} s  ${s.fichier} › ${s.test}${aucun ? '  (aucun test trouvé)' : ''}`,
  );
  console.log(lignes.at(-1));
}
for (const f of fautes) console.log(`FAUTE  ${f}`);
console.log(
  `\n${String(choix.length - ratees)}/${String(choix.length)} sondes prises · ${String(fautes.length)} faute(s) d'inscription`,
);
process.exit(ratees || fautes.length ? 1 : 0);

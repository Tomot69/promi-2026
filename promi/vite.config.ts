import { existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { defineConfig } from 'vite';

// L0 : une construction pour l'appareil sans état embarqué est refusée (l'app démarrerait sans les données de Tom)
if (process.env['APPAREIL'] && !existsSync('src/donnees/etat-embarque.json'))
  throw new Error('construction pour l’appareil : src/donnees/etat-embarque.json manque (npm run embarquer)');

// R3 : la version construite (le commit, « + » si l'arbre de travail est modifié), que l'app écrit au démarrage (`promi_version`) — sur
// l'iPhone elle se relit dans son stockage, recopié sur le Mac (`outils/version-iphone.sh`) : la version installée se VÉRIFIE
const lire = (c: string): string => {
  try {
    return execSync(c, { encoding: 'utf8' }).trim();
  } catch {
    return '';
  }
};
const VERSION = (lire('git rev-parse --short HEAD') || 'inconnu') + (lire('git status --porcelain -- src') ? '+' : '');

export default defineConfig({
  base: './',
  define: { __PROMI_VERSION__: JSON.stringify(VERSION) },
  build: { target: 'safari16', outDir: 'dist', assetsInlineLimit: 0, chunkSizeWarningLimit: 4000 },
  server: { host: '0.0.0.0', port: 5179, strictPort: true },
  preview: { host: '127.0.0.1', port: 5180, strictPort: true },
});

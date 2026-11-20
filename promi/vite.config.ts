import { existsSync } from 'node:fs';
import { defineConfig } from 'vite';

// L0 : une construction pour l'appareil sans état embarqué est refusée (l'app démarrerait sans les données de Tom)
if (process.env['APPAREIL'] && !existsSync('src/donnees/etat-embarque.json'))
  throw new Error('construction pour l’appareil : src/donnees/etat-embarque.json manque (npm run embarquer)');

export default defineConfig({
  base: './',
  build: { target: 'safari16', outDir: 'dist', assetsInlineLimit: 0, chunkSizeWarningLimit: 4000 },
  server: { host: '0.0.0.0', port: 5179, strictPort: true },
  preview: { host: '127.0.0.1', port: 5180, strictPort: true },
});

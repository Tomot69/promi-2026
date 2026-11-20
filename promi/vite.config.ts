import { defineConfig } from 'vite';

export default defineConfig({
  base: './',
  build: { target: 'safari16', outDir: 'dist', assetsInlineLimit: 0, chunkSizeWarningLimit: 4000 },
  server: { host: '0.0.0.0', port: 5179, strictPort: true },
  preview: { host: '127.0.0.1', port: 5180, strictPort: true },
});

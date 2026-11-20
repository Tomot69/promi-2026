import { defineConfig, devices } from '@playwright/test';

/**
 * Les tests de rendu : la vraie app (construite, `vite preview`, port 5180) comparée au prototype (la racine du dépôt, servie telle
 * quelle, port 8753), dans le MÊME navigateur : WebKit, celui de l'iPhone.
 */
export default defineConfig({
  testDir: 'tests/rendu',
  outputDir: 'test-results',
  timeout: 15 * 60 * 1000,
  fullyParallel: true,
  workers: process.env['CI'] ? 2 : 4,
  reporter: [['list']],
  use: { ...devices['Desktop Safari'], browserName: 'webkit' },
  webServer: [
    { command: 'npx vite preview --port 5180 --strictPort', url: 'http://127.0.0.1:5180/', reuseExistingServer: true },
    {
      command: 'python3 -m http.server 8753 --bind 127.0.0.1 --directory ..',
      url: 'http://127.0.0.1:8753/app.html',
      reuseExistingServer: true,
    },
  ],
});

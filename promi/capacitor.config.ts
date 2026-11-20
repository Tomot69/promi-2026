import type { CapacitorConfig } from '@capacitor/cli';

/**
 * La coquille native de la vraie app (Capacitor, retenu par Tom le 18 nov. 2026 — PREUVE-CAPACITOR.md).
 * iOS : signée avec le profil gratuit de Tom (équipe B77VBMD9BF), à re-signer chaque semaine. Android : préparé (aucune console Google).
 * L'inspection de la vue web (Safari › Développement) reste allumée : R3, « ce que le banc ne voit pas se voit sur l'iPhone de Tom ».
 */
const config: CapacitorConfig = {
  appId: 'fr.autier.promi',
  appName: 'Promi',
  webDir: 'dist',
  ios: { contentInset: 'never', scrollEnabled: false, webContentsDebuggingEnabled: true },
  android: { webContentsDebuggingEnabled: true },
  plugins: {
    StatusBar: { overlaysWebView: true },
    LocalNotifications: { presentationOptions: ['banner', 'sound'] },
  },
};

export default config;

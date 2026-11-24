/// <reference types="vite/client" />
declare module '*.js?raw' {
  const texte: string;
  export default texte;
}

/** la version construite (vite.config.ts) : le commit, « + » si `src` était modifié */
declare const __PROMI_VERSION__: string;

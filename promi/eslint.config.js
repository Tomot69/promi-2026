// Le lint de la vraie app. Il porte trois règles de l'architecture (ARCHITECTURE.md, CLAUDE.md « la vraie app sera propre ») :
//  · une seule horloge : hors de src/animation/horloge.ts, aucun setTimeout, setInterval, requestAnimationFrame, requestIdleCallback ;
//  · le moteur derrière sa façade : hors de src/moteur/, personne ne touche `Toile` ni `window.Toile` ;
//  · aucun écran n'importe un autre écran, ni le moteur repris.
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import globals from 'globals';

const MINUTERIES = ['setTimeout', 'setInterval', 'requestAnimationFrame', 'requestIdleCallback'].map((name) => ({
  name,
  message: 'Une seule horloge : passer par src/animation/horloge.ts (horloge().minuteur, .image, .quandLibre).',
}));

export default tseslint.config(
  {
    ignores: [
      'dist',
      'ios',
      'android',
      'node_modules',
      'src/**/repris/**',
      'test-results',
      'playwright-report',
      'src/design/jetons.ts',
    ],
  },
  js.configs.recommended,
  ...tseslint.configs.strictTypeChecked.map((c) => ({ ...c, files: ['src/**/*.ts'] })),
  ...tseslint.configs.recommended.map((c) => ({ ...c, files: ['tests/**/*.ts', 'outils/**/*.ts', '*.ts'] })),
  {
    files: ['src/**/*.ts'],
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      '@typescript-eslint/restrict-template-expressions': ['error', { allowNumber: true }],
      '@typescript-eslint/restrict-plus-operands': ['error', { allowNumberAndString: true }],
      // avec `noUncheckedIndexedAccess`, un indice qu'on vient de borner s'affirme ; c'est l'usage, pas une paresse
      '@typescript-eslint/no-non-null-assertion': 'off',
      // les données venues d'un export ou du stockage sont typées APRÈS lecture : les gardes défensives restent, même si le type les croit inutiles
      '@typescript-eslint/no-unnecessary-condition': 'off',
      '@typescript-eslint/no-unnecessary-type-conversion': 'off',
      'no-restricted-globals': [
        'error',
        ...MINUTERIES,
        { name: 'Toile', message: 'Le moteur passe par sa façade (src/moteur/facade.ts).' },
      ],
      'no-restricted-properties': [
        'error',
        ...MINUTERIES.map((m) => ({ object: 'window', property: m.name, message: m.message })),
        { object: 'window', property: 'Toile', message: 'Le moteur passe par sa façade (src/moteur/facade.ts).' },
      ],
      'no-restricted-imports': [
        'error',
        { patterns: [{ group: ['**/repris/*'], message: 'Une pièce reprise ne se charge que par son interface.' }] },
      ],
    },
  },
  { files: ['src/animation/horloge.ts'], rules: { 'no-restricted-properties': 'off', 'no-restricted-globals': 'off' } },
  {
    files: ['src/moteur/**', 'src/animation/trace/**', 'src/animation/flaques/**'],
    rules: { 'no-restricted-imports': 'off', 'no-restricted-properties': 'off' },
  },
  {
    files: ['src/ecrans/**'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: ['**/ecrans/*', '**/repris/*'],
              message: "Un écran n'importe ni un autre écran, ni le moteur repris.",
            },
          ],
        },
      ],
    },
  },
  {
    files: ['tests/**', '*.config.*', 'outils/**'],
    rules: {
      'no-restricted-globals': 'off',
      'no-restricted-properties': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
      '@typescript-eslint/no-unsafe-member-access': 'off',
      '@typescript-eslint/no-unsafe-call': 'off',
      '@typescript-eslint/no-unsafe-argument': 'off',
      '@typescript-eslint/no-non-null-assertion': 'off',
    },
  },
  { files: ['eslint.config.js'], ...tseslint.configs.disableTypeChecked },
);

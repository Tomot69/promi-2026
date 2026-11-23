/**
 * LE RETOUR HAPTIQUE (E3, C-077 ; le prototype : `window.promiHaptique`, un crochet vide dans Safari ; la preuve Capacitor — validée par Tom sur
 * son iPhone, C-291 — le branche sur le module Haptics : un impact fort quand une parole est tenue). Dans un navigateur : rien.
 */
import { Capacitor } from '@capacitor/core';
import { Haptics, ImpactStyle } from '@capacitor/haptics';

export type MomentHaptique = 'tenir';

export function haptique(nom: MomentHaptique): void {
  if (!Capacitor.isNativePlatform()) return;
  if (nom === 'tenir') Haptics.impact({ style: ImpactStyle.Heavy }).catch(() => undefined);
}

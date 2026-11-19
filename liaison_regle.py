"""⚑ v212 (C-312) — la règle de « de » / « d’ », écrite EN DUR pour les juges (redteam_liaison_exemples, redteam_liaison) : la même que `_promiElide`, la même liste de h aspirés (v210 §6).
Un juge porte la décision, il ne la relit pas dans l'app."""
import re, unicodedata
H_ASPIRE = set('hurler hair hausser heurter hisser hater harceler hacher hanter heler honte haine hasard hasarder haleter happer harasser hennir herisser hocher huer hululer hurle hais hait hate haut hors huit heros hockey harponner heurte'.split())
def norme(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower().replace('æ', 'ae').replace('œ', 'oe')) if unicodedata.category(c) != 'Mn')
def attendu(txt):
    m = re.match(r"^[^\s’'\"“«(]+", txt.strip())
    if not m: return 'de'
    w = re.sub(r'[^a-z0-9]', '', norme(m.group(0)))
    if not w: return 'de'
    c = w[0]
    if c.isdigit() or w in ('onze', 'onzieme', 'oui'): return 'de'
    if w in ('y', 'en'): return 'd’'
    if c == 'y': return 'de'
    if c == 'h': return 'de' if w in H_ASPIRE else 'd’'
    return 'd’' if c in 'aeiou' else 'de'

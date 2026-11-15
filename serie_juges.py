"""La série de juges d'un lot (C-227) : un juge à la fois, 10 minutes au plus chacun.

Usage : python3 serie_juges.py <dossier de sortie> <liste>
Chaque ligne de la liste : « nom | env | commande » (env : 1, 079, tom).

⚑ v198 (§0, Tom) — UN JUGE FERME SON NAVIGATEUR EN FIN DE PASSE, MÊME EN ÉCHEC OU AU-DELÀ DES 10 MINUTES.
Chaque juge tourne dans SON groupe de processus (start_new_session) ; à sa fin — normale, en erreur ou arrêtée à
10 min — tout le groupe est arrêté (SIGTERM, puis SIGKILL) : le pilote Playwright et ses WebKit / Chromium ne
peuvent plus survivre en orphelins (`subprocess.run(timeout=…)` ne tuait que le Python du juge). Le nombre de
processus arrêtés ainsi est écrit dans le journal (« orphelins : n »).
"""
import subprocess, sys, os, time, signal

D = sys.argv[1]; os.makedirs(D, exist_ok=True)
E079 = {'PYTHONPATH': 'scratchpad/v186/echelle079', 'PROMI_ECHELLE': '0,79'}
ETOM = {'PYTHONPATH': 'scratchpad/v190/fenetretom', 'PROMI_ECHELLE': 'tom'}
PLAFOND = int(os.environ.get("PLAFOND_JUGE", "600"))


def groupe(pgid):
    """les processus encore vivants du groupe du juge"""
    try:
        out = subprocess.run(['ps', '-axo', 'pid=,pgid='], capture_output=True, text=True).stdout
    except Exception:
        return []
    return [int(a) for a, b in (l.split() for l in out.splitlines() if l.strip()) if int(b) == pgid]


def ferme(pgid):
    """arrête tout le groupe : d'abord poliment, puis de force"""
    n = len(groupe(pgid))
    for sig, attente in ((signal.SIGTERM, 3.0), (signal.SIGKILL, 1.0)):
        vivants = groupe(pgid)
        if not vivants:
            break
        for pid in vivants:   # un par un : killpg est refusé dans le bac à sable (EPERM)
            try:
                os.kill(pid, sig)
            except (ProcessLookupError, PermissionError):
                pass
        t0 = time.time()
        while groupe(pgid) and time.time() - t0 < attente:
            time.sleep(0.2)
        if not groupe(pgid):
            break
    return n


J = []
for l in open(sys.argv[2]):
    l = l.strip()
    if not l or l.startswith('#'):
        continue
    nom, env, cmd = l.split('|', 2)
    J.append((nom.strip(), env.strip(), cmd.strip()))

log = open(D + '.log', 'a')
for nom, env, cmd in J:
    e = dict(os.environ); e.update({'079': E079, 'tom': ETOM}.get(env, {}))
    t = time.time(); f = open('%s/%s.txt' % (D, nom), 'w')
    p = subprocess.Popen(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT, env=e, start_new_session=True)
    try:
        p.wait(timeout=PLAFOND); st = 'fini'
    except subprocess.TimeoutExpired:
        st = 'NON JUGÉ (10 min)'
    orph = ferme(p.pid)   # le groupe porte le pid du shell qui l'a ouvert
    try:
        p.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass
    f.close()
    last = [x for x in open('%s/%s.txt' % (D, nom), errors='ignore').read().splitlines() if x.strip()][-1:]
    log.write('%-28s %-18s %5ds  orphelins : %d  %s\n' % (nom, st, time.time() - t, orph, (last[0][:100] if last else '')))
    log.flush()
log.write('FIN\n'); log.close()

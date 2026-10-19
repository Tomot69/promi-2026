#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
o=scratchpad/v152/suite.txt; : > $o
for f in app.html zz-av151.html; do
  a=$(sysctl -n vm.loadavg | awk '{print $2}')
  python3 redteam_guide.py --fichier=$f > scratchpad/v152/serie/guide-$f.log 2>&1
  echo "guide $f · charge $a · $(grep -E '❌|✅ +[0-9]+ / ' scratchpad/v152/serie/guide-$f.log | tr '\n' '|' | cut -c1-600)" >> $o
done
for i in 1 2 3; do for f in zz-av150.html app.html; do
  a=$(sysctl -n vm.loadavg | awk '{print $2}')
  python3 redteam_peaufiner.py --fichier=$f > scratchpad/v152/serie/peauf-$f-$i.log 2>&1
  echo "peaufiner $f #$i · charge $a · $(grep -E '❌|✅ +[0-9]+ / ' scratchpad/v152/serie/peauf-$f-$i.log | tr '\n' '|' | cut -c1-400)" >> $o
done; done
echo FIN >> $o

import sys; sys.argv=['banc_rendu.py','--monde=chamade']
import importlib.util
spec=importlib.util.spec_from_file_location('b','banc_rendu.py'); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
r1,_=b.passe(b.URL,['chamade']); b.range_(r1,'scratchpad/ch1')
r2,_=b.passe(b.URL,['chamade']); b.range_(r2,'scratchpad/ch2')
for n in ('toile-sombre','toile-clair'):
    print(n, b.ecart_pixels('scratchpad/ch1/chamade__%s.png'%n,'scratchpad/ch2/chamade__%s.png'%n))

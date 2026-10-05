import io
S=io.open('redteam_decoupe.py',encoding='utf-8').read()
old="""          window.__g2.push({pid:pid, monde:Toile.getTheme(), n:n, autres:+(100*au/n).toFixed(2), ecran:window.__g2e||''}); } } }catch(e){}"""
new="""          const pp=(typeof promises!=='undefined')?promises.find(x=>x.id===pid):null, mi=dcv.__dalleInfo&&dcv.__dalleInfo.monde;
          window.__g2.push({pid:pid, monde:Toile.getTheme(), n:n, autres:+(100*au/n).toFixed(2), ecran:window.__g2e||'', qui:(pp?pp.title:'(pas une parole)')+' · '+w+'×'+h+' · monde peint '+(mi?mi.m:'non déclaré')+' · '+JSON.stringify(opts||{}).slice(0,60)}); } } }catch(e){}"""
assert S.count(old)==1; S=S.replace(old,new)
old="""                    print('  %s  %-9s %-5s %-26s %3d dalle(s) rendue(s) · au pire %.2f %% de pixels d\\'une autre couleur' % ('OK' if bon else 'KO', m, th, nom, len(L), pire))"""
new="""                    print('  %s  %-9s %-5s %-26s %3d dalle(s) rendue(s) · au pire %.2f %% de pixels d\\'une autre couleur' % ('OK' if bon else 'KO', m, th, nom, len(L), pire))
                    if not bon:      # un instrument NOMME ce qui rate (§8)
                        for r in sorted(L, key=lambda r: -r['autres'])[:3]:
                            if r['autres'] > G2_MAX: print('        ↳ %.2f %% · %s' % (r['autres'], r.get('qui', '')))"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('redteam_decoupe.py','w',encoding='utf-8').write(S)

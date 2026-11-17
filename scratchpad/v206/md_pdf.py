"""un rendu minimal Markdown → PDF (titres, tableaux, listes, gras, code), pour lire les documents du lot dans Aperçu"""
import re, sys, html
from playwright.sync_api import sync_playwright
def inline(t):
    t = html.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t); t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t); t = re.sub(r'(?<![\w*])\*([^*]+)\*(?![\w*])', r'<i>\1</i>', t)
    return t
def rendu(md):
    out, L, i = [], md.split('\n'), 0
    while i < len(L):
        l = L[i]
        if l.startswith('|'):
            rows = []
            while i < len(L) and L[i].startswith('|'): rows.append(L[i]); i += 1
            cells = [[c.strip() for c in r.strip('|').split('|')] for r in rows if not re.match(r'^\|[\s|:-]+\|$', r)]
            out.append('<table>' + ''.join('<tr>' + ''.join(('<th>' if k == 0 else '<td>') + inline(c) + ('</th>' if k == 0 else '</td>') for c in r) + '</tr>' for k, r in enumerate(cells)) + '</table>'); continue
        m = re.match(r'^(#{1,4}) (.*)', l)
        if m: out.append('<h%d>%s</h%d>' % (len(m.group(1)), inline(m.group(2)), len(m.group(1))))
        elif re.match(r'^\s*(- |\d+\. )', l): out.append('<li>' + inline(re.sub(r'^\s*(- |\d+\. )', '', l)) + '</li>')
        elif l.startswith('>'): out.append('<blockquote>' + inline(l.lstrip('> ')) + '</blockquote>')
        elif l.startswith('```'): pass
        elif l.strip(): out.append('<p>' + inline(l) + '</p>')
        i += 1
    return '\n'.join(out)
CSS = "body{font:11px/1.45 -apple-system,Helvetica,sans-serif;margin:28px;color:#201908} h1{font-size:19px} h2{font-size:15px;margin-top:18px} h3{font-size:13px} table{border-collapse:collapse;margin:8px 0;width:100%} td,th{border:1px solid #ccc;padding:3px 5px;vertical-align:top;font-size:9.5px} th{background:#f3ece0} code{font:9.5px Menlo,monospace;background:#f5f0e6} li{margin-left:16px} blockquote{border-left:3px solid #ccc;margin:4px 0;padding-left:8px}"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for src in sys.argv[1:]:
        pg.set_content('<meta charset=utf-8><style>' + CSS + '</style>' + rendu(open(src, encoding='utf-8').read()))
        pg.pdf(path='scratchpad/v206/' + src.replace('.md', '.pdf'), format='A4', margin={'top': '12mm', 'bottom': '12mm', 'left': '10mm', 'right': '10mm'}); print('ok', src)
    b.close()

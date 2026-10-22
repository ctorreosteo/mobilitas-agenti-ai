# Rende una bozza Superdesign visibile offline nel visore locale, con le foto reali.
# 1) Tailwind, Iconify e Montserrat dalla cartella vendor/ del visore (copiata da tools/superdesign/visore/vendor).
# 2) Segnaposto https://placehold.co/...?text=<nome>  ->  foto/<nome>.jpg o recensioni/<nome>.jpg (file locali reali).
# Non tocca layout né testi. Elenca gli indirizzi esterni rimasti e i segnaposto senza file.
# Uso: python3 -I localizza-bozza.py <bozza.html> <visore/pagina.html>
import os
import re
import sys

src, out = sys.argv[1], sys.argv[2]
base = os.path.dirname(os.path.abspath(out))
h = open(src, encoding='utf-8').read()
h = h.replace('https://cdn.tailwindcss.com', '/vendor/tailwind-play.js')
h = re.sub(r'https://code\.iconify\.design/iconify-icon/[^"\']+', '/vendor/iconify-icon.min.js', h)
h = re.sub(r'https://(?:fonts\.googleapis\.com/css2?|api\.fontshare\.com/v2/css)\?[^"\']*', '/vendor/montserrat.css', h)
h = re.sub(r'<link[^>]+(?:fonts\.gstatic\.com|fonts\.googleapis\.com)"[^>]*>\s*', '', h)
mancanti = []


def foto(m):
    nome = m.group(1).split('&')[0]
    for cart in ('foto', 'recensioni'):
        for est in ('.jpg', '.jpeg', '.png', '.webp'):
            if os.path.exists(os.path.join(base, cart, nome + est)):
                return f'{cart}/{nome}{est}'
    mancanti.append(nome)
    return m.group(0)


h = re.sub(r'https://placehold\.co/[^"\'\s?]+\?text=([A-Za-z0-9_-]+(?:&[^"\'\s]*)?)', foto, h)
resto = sorted(set(re.findall(r'https?://[^\s"\'()<>]+', h)))
open(out, 'w', encoding='utf-8').write(h)
print('segnaposto senza file:', *(mancanti or ['nessuno']), sep='\n  ')
print('indirizzi esterni rimasti nel testo (verifica che non vengano caricati):', *(resto or ['nessuno']), sep='\n  ')

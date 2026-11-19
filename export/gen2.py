#!/usr/bin/env python3
"""Sitio estático responsive (celular = V2, computadora = Desktop) a partir de los archivos de Claude Design."""
import re, json, os, shutil, subprocess
from PIL import Image

S = os.environ.get('KIT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = S + '/export/site'
FS = S + '/render/node_modules/@fontsource'
BREAK = 1280  # desde este ancho se muestra la versión de computadora

shutil.rmtree(OUT, ignore_errors=True)
for d in ['assets/css', 'assets/js', 'assets/img', 'assets/fonts']:
    os.makedirs(OUT + '/' + d)

def vals(src, state):
    out = subprocess.run(['node', '-e', r'''
const fs=require('fs');const s=fs.readFileSync(process.argv[1],'utf8');
const js=s.slice(s.indexOf('class Component'),s.lastIndexOf('</script>'));
const C=new Function('DCLogic',js+';return Component;')(class{});
const c=new C();c.state=JSON.parse(process.argv[2]);
process.stdout.write(JSON.stringify(c.renderVals()));''', src, json.dumps(state)], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)

DATEIF = {'showThanks': '2026-11-26', 'showNoche': '2026-12-24',
          'showFin': '2026-12-31', 'showBrunch': '2027-01-01', 'showSS': '2026-12-27'}
tok = re.compile(r'<sc-for list="\{\{\s*([\w.]+)\s*\}\}" as="(\w+)"[^>]*>|</sc-for>|<sc-if value="\{\{\s*([\w.]+)\s*\}\}"[^>]*>|</sc-if>')

def esc(v):
    return str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def look(path, c):
    v = c
    for k in path.split('.'):
        v = v.get(k, '') if isinstance(v, dict) else ''
    return v

def build(fname):
    src_path = S + '/canvas/project/' + fname
    src = open(src_path, encoding='utf-8').read()
    style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
    body = src[src.index('</helmet>') + 9:src.index('</x-dc>')]
    js = src[src.index('class Component'):]

    # ids reales de zonas y lugares
    zone_ids, place_ids = [], {}
    cur = None
    for m in re.finditer(r"\{ id: '(\w+)', (label|name): ", js[js.index('var zonasData'):js.index('var zonaTabs')]):
        if m.group(2) == 'label':
            cur = m.group(1); zone_ids.append(cur); place_ids[cur] = []
        else:
            place_ids[cur].append(m.group(1))

    base = vals(src_path, {})
    for t, tid in zip(base['tiers'], ['access', 'classic', 'experience']):
        t['id'] = tid; t['hid'] = '' if t['open'] else 'hidden'; t['open'] = True
    zonas = []
    for i, zid in enumerate(zone_ids):
        z = vals(src_path, {'zona': zid})['zona']
        z['id'] = zid; z['hid'] = '' if i == 0 else 'hidden'
        assert len(z['items']) == len(place_ids[zid]), zid
        for it, pid in zip(z['items'], place_ids[zid]):
            it['pid'] = pid
        zonas.append(z)
    for z, zid in zip(base['zonaTabs'], zone_ids):
        z['id'] = zid
    ctx = dict(base); ctx['zonas'] = zonas

    def rep(a, b, n=1):
        nonlocal body
        c = body.count(a)
        assert c == n, (fname, a[:90], c)
        body = body.replace(a, b)

    # raíz
    body, k = re.subn(r'<div style="width: 100%; max-width: (\d+)px; margin: 0 auto; min-height: \d+px;', r'<div style="width: 100%; max-width: \1px; margin: 0 auto;', body, count=1)
    assert k == 1, fname

    # Day Pass
    rep('<div style="border-bottom: 1px solid var(--ac-dark-beige); display: flex; flex-direction: column">\n<button type="button" onClick="{{t.pick}}"',
        '<div data-tier-box="{{t.id}}" style="border-bottom: 1px solid var(--ac-dark-beige); display: flex; flex-direction: column">\n<button type="button" data-tier="{{t.id}}" aria-controls="tier-{{t.id}}"')
    rep('<div style="padding: 2px 2px 22px;', '<div id="tier-{{t.id}}" {{t.hid}} style="padding: 2px 2px 22px;')

    # Tarjetas que giran
    for n in ('1', '2'):
        rep('transform: rotateY({{f%s}}deg)">' % n, 'transform: rotateY({{f%s}}deg)" data-flip-card="%s">' % (n, n))
        rep('onClick="{{flip%s}}"' % n, 'data-flip="%s"' % n, 2)

    # Alrededores
    rep('onClick="{{z.pick}}"', 'data-zona-tab="{{z.id}}" aria-controls="zona-{{z.id}}"')
    a = body.index('{{zona.title}}</div>')
    a = body.rfind('<div ', 0, a)
    b = body.index('</ul>', a) + 5
    body = body[:a] + '<sc-for list="{{zonas}}" as="zona"><div id="zona-{{zona.id}}" data-zona-panel="{{zona.id}}" {{zona.hid}}>' + body[a:b] + '</div></sc-for>' + body[b:]
    rep('onClick="{{it.toggle}}"', 'data-place="{{it.pid}}" aria-controls="place-{{it.pid}}"')
    rep('<sc-if value="{{it.open}}" hint-placeholder-val="{{false}}">\n<div style="padding: 0 2px 16px;',
        '<sc-if value="{{it.hasInside}}" hint-placeholder-val="{{false}}">\n<div id="place-{{it.pid}}" hidden style="padding: 0 2px 16px;')

    # Agenda y fechas
    rep('href="{{agenda.href}}"', 'href="{{agenda.href}}" data-agenda-link data-fest-name="{{agenda.festName}}"')
    rep('color: {{agenda.eyebrow}}">Próximo', 'color: {{agenda.eyebrow}}" data-agenda-eyebrow>Próximo')
    rep('{{agenda.when}}', '<span data-agenda="when">{{agenda.when}}</span>')
    rep('{{agenda.name1}}', '<span data-agenda="name1">{{agenda.name1}}</span>')
    rep('{{agenda.name2}}', '<span data-agenda="name2">{{agenda.name2}}</span>')
    for _k, _d in (('cdThanks', '2026-11-26'), ('cdNoche', '2026-12-24'), ('cdSS', '2026-12-27'), ('cdFin', '2026-12-31')):
        if '{{ %s }}' % _k in body: rep('{{ %s }}' % _k, '<span data-countdown="%s"></span>' % _d)
    rep('{{nextLastSunday}}', '<span data-lastsunday>{{nextLastSunday}}</span>')

    # Borradores fuera del público
    assert '[HORA]' not in body and '#inscripcion' not in body, fname
    _pend = [x for x in ('[Qué incluye]', '[Precio]', '[fecha]', '[por confirmar') if x in body]
    assert not _pend, ('Faltan datos por completar', fname, _pend)

    # <main>
    i = body.index('<sc-if value="{{hasAgenda}}"'); j = body.index('<footer')
    body = body[:i] + '<main style="display: flex; flex-direction: column">\n' + body[i:j] + '</main>\n' + body[j:]

    def parse(i):
        out = []
        while True:
            m = tok.search(body, i)
            if not m:
                out.append(body[i:]); return out, len(body)
            out.append(body[i:m.start()]); i = m.end(); t = m.group(0)
            if t.startswith('</'):
                return out, i
            kids, i = parse(i)
            out.append(('for', m.group(1), m.group(2), kids) if t.startswith('<sc-for') else ('if', m.group(3), kids))

    def render(nodes, c):
        r = ''
        for n in nodes:
            if isinstance(n, str):
                r += re.sub(r'\{\{\s*([\w.$]+)\s*\}\}', lambda m: esc(look(m.group(1), c)), n)
            elif n[0] == 'for':
                for it in look(n[1], c):
                    r += render(n[3], {**c, n[2]: it})
            else:
                k = n[1]
                if k in DATEIF:
                    r += '<div data-until="%s" style="display: contents">' % DATEIF[k] + render(n[2], c) + '</div>'
                elif k == 'hasAgenda':
                    r += '<div data-agenda-wrap style="display: contents">' + render(n[2], c) + '</div>'
                elif k == 'agenda.fest':
                    r += '<div data-feria style="display: contents">' + render(n[2], c) + '</div>'
                elif k == 'noSeason':
                    r += '<div data-noseason hidden>' + render(n[2], c) + '</div>'
                elif look(k, c):
                    r += render(n[2], c)
        return r

    tree, _ = parse(0)
    html = render(tree, ctx).replace(' hidden=""', ' hidden')
    left = re.findall(r'\{\{[^}]*\}\}|onClick|<sc-|\[HORA\]|#inscripcion', html)
    assert not left, (fname, left[:5])
    return html, style

# Versión a publicar: VERSION=navidad usa V2-navidad / Desktop-navidad
_v = os.environ.get('VERSION', '')
_sfx = ('-' + _v) if _v else ''
mob, style = build('V2%s.dc.html' % _sfx)
desk, _ = build('Desktop%s.dc.html' % _sfx)

# ids únicos en la versión de computadora
ids = set(re.findall(r'\sid="([^"]+)"', desk))
for i in sorted(ids, key=len, reverse=True):
    desk = desk.replace('id="%s"' % i, 'id="d-%s"' % i).replace('href="#%s"' % i, 'href="#d-%s"' % i)
    desk = desk.replace('aria-controls="%s"' % i, 'aria-controls="d-%s"' % i).replace('url(#%s)' % i, 'url(#d-%s)' % i)
dup = set(re.findall(r'\sid="([^"]+)"', mob)) & set(re.findall(r'\sid="([^"]+)"', desk))
assert not dup, dup

html = ('<div class="v-m" data-pfx="">\n' + mob.strip() + '\n</div>\n<div class="v-d" data-pfx="d-">\n' + desk.strip() + '\n</div>')

# ---------- imágenes ----------
BLOB = {'cd3223e51e4f9c01af4b9797a88786f6': ('hero-hotel.jpg', 'portada-hotel', 1600),
        'e817ff1320514e50999ebafd97733fc1': ('ac-logo-white.png', 'ac-logo', 0),
        '7dba6cfb0411723b68da8ee5eb50cb2e': ('daypass-flamenco.jpg', 'day-pass', 1000),
        'b69dd9c91f97c30b752834dcad247f99': ('real-thanksgiving.jpg', 'thanksgiving', 900),
        'b1aef0b756c24e6b2189b008c2b02ba7': ('real-arbol.jpg', 'nochebuena', 0),
        '5afe661ac36a6e9b2d608f682e37d278': ('fin-de-ano.jpg', 'fin-de-ano', 0),
        '5c1e8edad722490adac45253bcf680fb': ('brunch.jpg', 'brunch', 0),
        'f209d0c0a8820090a35eacb573d327b8': ('real-taco.jpg', 'taco-tuesday', 720),
        '081193769b9b95f9a3ecaf052210c4d9': ('real-buffet.jpg', 'last-sunday', 720),
        '6b812dc5cb012d29bd35564342d6c71d': ('especiales-vino.jpg', 'especiales', 720),
        '0599d89ecfb27a3c4c5cdca812bc909a': ('business-desayuno.jpg', 'business-point', 1100)}
used = set(re.findall(r'/_blob/([0-9a-f]+)', html))
assert used <= set(BLOB), used - set(BLOB)
for bid in used:
    fn, name, w = BLOB[bid]
    if fn.endswith('.png'):
        shutil.copy(S + '/img/' + fn, OUT + '/assets/img/' + name + '.png')
        html = html.replace('/_blob/' + bid, '/assets/img/' + name + '.png'); continue
    im = Image.open(S + '/img/' + fn).convert('RGB')
    if w == 0:
        h = min(420, im.height); im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    elif im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(OUT + '/assets/img/' + name + '.webp', 'WEBP', quality=(70 if name == 'portada-hotel' else 78), method=6)
    html = html.replace('/_blob/' + bid, '/assets/img/' + name + '.webp')
def lazy(m):
    tag = m.group(0)
    if 'portada-hotel' in tag or 'ac-logo' in tag:
        return tag.replace('<img ', '<img decoding="async" ', 1)
    return tag.replace('<img ', '<img loading="lazy" decoding="async" ', 1)
html = re.sub(r'<img [^>]*>', lazy, html)

og = Image.open(S + '/img/hero-hotel.jpg').convert('RGB')
tw, th = 1200, 630
sc = max(tw / og.width, th / og.height)
og = og.resize((round(og.width * sc), round(og.height * sc)), Image.LANCZOS)
top = int((og.height - th) * 0.5)
og.crop(((og.width - tw) // 2, top, (og.width - tw) // 2 + tw, top + th)).save(OUT + '/assets/img/compartir-hotel.jpg', quality=82)
logo = Image.open(S + '/img/ac-logo-white.png').convert('RGBA')
fav = Image.new('RGBA', (192, 192), (28, 28, 28, 255))
lw = 150; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
fav.alpha_composite(logo, ((192 - lw) // 2, (192 - logo.height) // 2))
fav.save(OUT + '/assets/img/icono.png')
fav.resize((48, 48), Image.LANCZOS).save(OUT + '/favicon.ico')

# ---------- fuentes ----------
faces = []
for fam, files in [('cormorant-garamond', ['400', '500', '600', '400-italic', '500-italic']),
                   ('montserrat', ['300', '400', '500', '600', '700']), ('work-sans', ['400', '500', '600'])]:
    for f in files:
        css = open('%s/%s/%s.css' % (FS, fam, f)).read()
        for block in re.findall(r'@font-face\s*\{[^}]*\}', css):
            if not re.search(r'-latin-\d', block):
                continue
            w2 = re.search(r'url\(\./files/([^)]+\.woff2)\)', block).group(1)
            shutil.copy('%s/%s/files/%s' % (FS, fam, w2), OUT + '/assets/fonts/' + w2)
            faces.append(re.sub(r'src:[^;]*;', "src: url(/assets/fonts/%s) format('woff2');" % w2, block))

# ---------- CSS ----------
tokens = ''.join(open(S + '/canvas/project/ds/ac/tokens/%s.css' % n, encoding='utf-8').read() for n in ['colors', 'typography', 'spacing'])
tokens = re.sub(r"@import url\([^)]*\);\s*", '', tokens)
style = style.replace('#servicios', '.v-d #d-servicios')  # hover de cortina solo en computadora
site_css = ('/* AC Hotel Punta Cana · landing */\n' + '\n'.join(faces) + '\n' + tokens + '\n' + style.strip() +
            '\n[hidden]{display:none !important}\na{color:#6E5A40}\n'
            'html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}\n'
            'body{background:#D9D2C8;min-height:100vh}\n'
            '.v-d{display:none}\n'
            '@media (min-width: ' + str(BREAK) + 'px){.v-m{display:none}.v-d{display:block}}\n'
            '@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}}\n'
            ':focus-visible{outline:2px solid #1C1C1C;outline-offset:2px}\n')
open(OUT + '/assets/css/site.css', 'w', encoding='utf-8').write(site_css)

# ---------- HTML ----------
SITE = 'https://ac-planes.vercel.app'
TITLE = 'AC Hotel Punta Cana · Piscina, cenas y eventos en Bávaro'
DESC = 'Day Pass, Taco Tuesday, Last Sunday Pool, cenas de temporada y espacios para empresas en AC Hotel Punta Cana, en el centro de Bávaro.'
head = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#1C1C1C">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_DO">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta name="robots" content="noindex, nofollow">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/assets/img/compartir-hotel.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="/assets/img/icono.png">
<link rel="preload" href="/assets/img/portada-hotel.webp" as="image">
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/app.js" defer></script>
<script src="/_vercel/insights/script.js" defer></script>
</head>
<body>
'''
html = re.sub(r'<a href="(https://www\.google\.com/maps/[^"]*)"(?![^>]*target=)', r'<a href="\1" target="_blank" rel="noopener noreferrer"', html)
html = re.sub(r'\n{3,}', '\n\n', html)

# ---- Medición de clics: los enlaces de salida pasan por /ir/<nombre>/ (cuenta como página en Vercel) ----
import html as _h, os as _os
EVENTOS = [('thanksgiving', 'Thanksgiving'), ('nochebuena', 'Nochebuena'),
           ('fin-de-ano', 'Fin de A'), ('brunch', 'Brunch de Bienvenida')]
DEST = {}
def _slug(t):
    import unicodedata
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')
def _nombre(pos, end, url, txt):
    before = html[:pos]; upto = html[:end]
    secs = [(m.start(), m.group(1)) for m in re.finditer(r'<section id="(?:d-)?([a-z]+)"', before)]
    sec = 'portada'
    if secs:
        st, sec = secs[-1]
        if before.count('</section>', st) > before.count('<section', st + 1): sec = 'pie'
    if 'privacy' in url: return None
    if 'calendar.google' in url: return ('nochebuena' if 'Nochebuena' in url else 'fin-de-ano' if 'Fin+de+A' in url else 'thanksgiving') + '-calendario'
    if 'rockthesport' in url: return 'san-silvestre-inscripcion'
    if 'google.com/maps' in url: return 'mapa-' + ('alrededores' if sec == 'llegar' else 'direccion')
    if sec == 'temporada' and 'take out' in txt.lower(): return 'whatsapp-nochebuena-takeout'
    if sec == 'temporada':
        ev, best = 'evento', -1
        for k, n in EVENTOS:
            i = upto.rfind(n)
            if i > best: ev, best = k, i
        return 'whatsapp-' + ev
    if sec == 'semana':
        return 'whatsapp-' + ('taco-tuesday' if before.rfind('Taco Tuesday') > before.rfind('Last Sunday') else 'last-sunday')
    if sec == 'pie': return 'whatsapp-pie-' + url[-4:]
    lab = {'empresas': 'business-point', 'daypass': 'day-pass', 'estadia': 'estadia'}.get(sec, sec)
    if 'Fin de a' in txt: lab = 'business-fin-de-ano'
    return 'whatsapp-' + lab
def _swap(m):
    url = _h.unescape(m.group(1)); txt = re.sub(r'<[^>]+>', ' ', m.group(2))
    n = _nombre(m.start(), m.end(), url, txt)
    if not n: return m.group(0)
    if n in DEST and DEST[n] != url: n = n + '-2'
    DEST[n] = url
    return m.group(0).replace('href="' + m.group(1) + '"', 'href="/ir/' + n + '/"', 1)
html = re.sub(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', _swap, html, flags=re.S)
IR_PAGE = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Abriendo…</title>
<meta http-equiv="refresh" content="3;url={u}">
<script src="/assets/js/ir.js" defer data-to="{u}"></script>
<script src="/_vercel/insights/script.js" defer></script>
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#FBF8F4;color:#1C1C1C;font:16px/1.5 system-ui,sans-serif;text-align:center;padding:16px}}a{{color:#80694C}}</style>
</head><body><p>Abriendo…<br><a href="{u}">Toca aquí si no se abre</a></p></body></html>
"""
_os.makedirs(OUT + '/ir', exist_ok=True)
for n, u in DEST.items():
    _os.makedirs(OUT + '/ir/' + n, exist_ok=True)
    open(OUT + '/ir/' + n + '/index.html', 'w', encoding='utf-8').write(IR_PAGE.format(u=_h.escape(u, quote=True)))
print('salidas:', sorted(DEST))
open(OUT + '/index.html', 'w', encoding='utf-8').write(head + html + '\n</body>\n</html>\n')
for a, b in [('app2.js', 'assets/js/app.js'), ('ir.js', 'assets/js/ir.js'), ('vercel.json', 'vercel.json'), ('gitignore.txt', '.gitignore'), ('README2.md', 'README.md')]:
    shutil.copy(S + '/export/' + a, OUT + '/' + b)
print('ok', len(html))

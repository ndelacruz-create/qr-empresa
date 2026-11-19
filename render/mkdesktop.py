#!/usr/bin/env python3
"""Deriva Desktop.dc.html (1280 px) a partir de V2.dc.html. Re-ejecutable cuando cambie V2."""
import re, sys, os
S = os.environ.get('KIT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_v = os.environ.get('VERSION', ''); _sfx = ('-' + _v) if _v else ''
s = open(S + '/canvas/project/V2%s.dc.html' % _sfx, encoding='utf-8').read()
H = int(sys.argv[1]) if len(sys.argv) > 1 else 5200

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (a[:90], c, n)
    s = s.replace(a, b)

def sec(start, end):
    i = s.index(start); j = s.index(end, i) + len(end)
    return i, j

# ---------- base ----------
rep('<title>Landing AC Hotel Punta Cana, celular, versión 2</title>', '<title>Landing AC Hotel Punta Cana, computadora</title>')
s = re.sub(r'<div style="width: 100%; max-width: 390px; margin: 0 auto; min-height: \d+px;', '<div style="width: 100%%; max-width: 1280px; margin: 0 auto; min-height: %dpx;' % H, s, count=1)
assert 'max-width: 1280px' in s
s = re.sub(r'"\$preview":\{"width":390,"height":\d+\}', '"$preview":{"width":1280,"height":%d}' % H, s, count=1)

# ---------- portada ----------
rep('<section style="position: relative; height: 440px; overflow: hidden;', '<section style="position: relative; height: 620px; overflow: hidden;')
rep('object-fit: cover; object-position: 38% 55%; animation: acZoom 12s', 'object-fit: cover; object-position: 50% 60%; animation: acZoom 12s')
rep('left: 8px; top: 8px; right: 8px; bottom: 8px; border: 1px solid rgba(255,255,255,0.55)', 'left: 18px; top: 18px; right: 18px; bottom: 18px; border: 1px solid rgba(255,255,255,0.55)')
rep('padding: 16px 16px 0; display: flex; align-items: flex-start; justify-content: center">', 'padding: 40px 48px 0; display: flex; align-items: flex-start; justify-content: center">')
rep('alt="AC Hotels by Marriott Punta Cana" style="height: 64px; width: auto">', 'alt="AC Hotels by Marriott Punta Cana" style="height: 84px; width: auto">')
rep('<div style="position: relative; margin-top: 34px; display: flex; flex-direction: column; align-items: center; text-align: center; padding: 0 24px">',
    '<div style="position: relative; margin-top: 64px; display: flex; flex-direction: column; align-items: center; text-align: center; padding: 0 24px">')
rep("font-size: min(40px, 10.2vw); line-height: 1.15; letter-spacing: 0.06em;", "font-size: 76px; line-height: 1.1; letter-spacing: 0.08em;", 2)
rep("<p style=\"margin: 12px 0 0; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 20px; line-height: 27px; animation: acRise 1s 0.7s",
    "<p style=\"margin: 20px 0 0; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 28px; line-height: 36px; animation: acRise 1s 0.7s")
# agenda
rep('style="position: relative; margin: -56px 16px 0; background: {{agenda.bg}};', 'style="position: relative; align-self: center; width: 480px; box-sizing: border-box; margin: -70px 0 0; background: {{agenda.bg}};')
# índice
rep('<div aria-hidden="true" style="margin: 22px 12px 0; display: flex;', '<div aria-hidden="true" style="align-self: center; width: 820px; margin: 40px 0 0; display: flex;')
rep('<nav aria-label="Ir a una sección" style="margin: 16px 12px 0; display: grid;', '<nav aria-label="Ir a una sección" style="align-self: center; width: 820px; margin: 32px 0 0; display: grid;')
rep('justify-content: flex-start; gap: 6px; min-height: 64px; padding: 10px 2px 8px;', 'justify-content: center; gap: 8px; min-height: 84px; padding: 10px 2px;', 5)
rep('<span style="font-family: var(--font-display); font-size: 10.5px; font-weight: 500; line-height: 13px; letter-spacing: 0.02em">', '<span style="font-family: var(--font-display); font-size: 12.5px; font-weight: 500; line-height: 16px; letter-spacing: 0.04em">', 5)

# ---------- la carta ----------
rep('<div id="carta" style="margin: 24px 8px 0; background: #FBF8F4;', '<div id="carta" style="align-self: center; width: 1200px; box-sizing: border-box; margin: 48px 0 0; background: #FBF8F4;')
rep('<div style="padding: 30px 20px 0; display: flex; gap: 12px; align-items: flex-start">', '<div style="align-self: center; width: 640px; padding: 48px 0 0; display: flex; gap: 16px; align-items: flex-start">')
rep("<p style=\"margin: 0; font-family: 'Cormorant Garamond', serif; font-size: 19px; line-height: 26px\"><span style=\"position: absolute;",
    "<p style=\"margin: 0; font-family: 'Cormorant Garamond', serif; font-size: 23px; line-height: 31px\"><span style=\"position: absolute;")

# títulos de sección: en una línea y más grandes
H2 = '<h2 style="margin: 0; display: flex; flex-direction: column; align-items: center; text-align: center">'
H2D = '<h2 style="margin: 0; display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; column-gap: 0.4em; text-align: center">'
s = s.replace(H2, H2D)
s = s.replace("font-size: 30px; line-height: 34px; letter-spacing: 0.1em; text-transform: uppercase", "font-size: 46px; line-height: 54px; letter-spacing: 0.1em; text-transform: uppercase")

# servicios: los 9 colgantes en una sola fila
rep('<section id="servicios" style="position: relative; z-index: 0; padding: 40px 20px 0;', '<section id="servicios" style="position: relative; z-index: 0; padding: 64px 40px 0;')
rep('</ul>\n<ul style="margin: 16px 0 0; padding: 0; list-style: none; display: flex; justify-content: space-between; border-top: 2px solid var(--ac-dark-beige)">\n', '', 2)
rep('<ul style="margin: 26px 0 0; padding: 0; list-style: none; display: flex; justify-content: space-between; border-top: 2px solid var(--ac-dark-beige)">',
    '<ul style="margin: 36px 0 0; padding: 0 6px; list-style: none; display: flex; justify-content: space-between; border-top: 2px solid var(--ac-dark-beige)">')
rep('<span style="width: 106px; min-height: 160px;', '<span style="width: 112px; min-height: 168px;', 9)

# ---------- Day Pass: foto a la izquierda, opciones a la derecha ----------
i, j = sec('<section id="daypass"', '</section>')
d = s[i:j]
d = d.replace('padding: 48px 20px 0; display: flex; flex-direction: column">', 'padding: 88px 40px 0; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); column-gap: 56px; align-items: start">')
d = d.replace(H2D, H2D.replace('margin: 0;', 'margin: 0; grid-column: 1 / -1;'))
d = d.replace('<p style="margin: 18px 0 0; text-align: center;', '<p style="grid-column: 1 / -1; margin: 14px 0 0; text-align: center;')
d = d.replace("font-style: italic; font-size: 20px; line-height: 26px\">Tres maneras", "font-style: italic; font-size: 24px; line-height: 30px\">Tres maneras")
d = d.replace('<div style="position: relative; margin-top: 26px">', '<div style="position: relative; margin-top: 36px">')
d = d.replace('<div style="height: 230px; overflow: hidden; border: 1px solid var(--ac-dark-beige); padding: 8px;', '<div style="height: 420px; overflow: hidden; border: 1px solid var(--ac-dark-beige); padding: 10px;')
d = d.replace('right: -6px; bottom: -40px; width: 108px;', 'right: -22px; bottom: -34px; width: 108px;')
d = d.replace('<div style="margin-top: 44px; display: flex; flex-direction: column">', '<div style="margin-top: 36px; display: flex; flex-direction: column">').replace('Toca una opción para ver qué incluye', 'Elige una opción para ver qué incluye')
assert d.count('grid-column: 1 / -1') == 2 and 'height: 420px' in d and 'margin-top: 36px; display: flex; flex-direction: column">' in d and 'Elige una opción' in d
s = s[:i] + d + s[j:]

# ---------- Temporada: tarjetas en rejilla ----------
i, j = sec('<section id="temporada"', '</section>')
d = s[i:j]
d = d.replace('padding: 44px 20px 0; display: flex; flex-direction: column">', 'padding: 96px 40px 0; display: flex; flex-direction: column">')
a = min(d.index(x) for x in ('<sc-if value="{{showThanks}}"', '<sc-if value="{{showNoche}}"', '<sc-if value="{{showFin}}"', '<sc-if value="{{showBrunch}}"') if x in d); b = d.index('<sc-if value="{{noSeason}}"')
grid = d[a:b]
SMALL = 'flex: 1 1 320px; max-width: 354px; box-sizing: border-box; '
n = 0
def r1(a_, b_, k=1, opt=False):
    global grid, n
    if opt and a_ not in grid: return
    assert grid.count(a_) == k, (a_[:70], grid.count(a_))
    grid = grid.replace(a_, b_); n += 1
r1('<article data-fest-card="1" style="position: relative; margin-top: 36px;', '<article data-fest-card="1" style="flex: 1 1 100%; max-width: 1118px; box-sizing: border-box; display: grid !important; grid-template-columns: 1fr 1fr; position: relative; margin-top: 0;', opt=True)
r1('<div aria-hidden="true" style="height: 14px; background:', '<div aria-hidden="true" style="grid-column: 1 / -1; height: 14px; background:', 2, opt=True)
r1('<div style="position: relative; height: 176px; overflow: hidden; margin: 14px 14px 0;', '<div style="position: relative; min-height: 470px; overflow: hidden; margin: 22px 0 22px 22px;', opt=True)
r1('style="width: 100%; height: 100%; object-fit: cover; display: block; animation: acZoom', 'style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; display: block; animation: acZoom', opt=True)
r1('right: 8px; top: 118px; z-index: 1; width: 104px; height: 104px;', 'right: auto; left: calc(50% - 96px); top: 40px; z-index: 1; width: 136px; height: 136px;', opt=True)
r1('left: 8px; top: 108px; z-index: 1; width: 104px; height: 104px;', 'left: 4px; top: 6px; z-index: 1; width: 136px; height: 136px;', opt=True)
r1('<svg width="104" height="104" viewBox="0 0 104 104"', '<svg width="136" height="136" viewBox="0 0 104 104"', opt=True)
r1('height: 46px; margin: 20px -18px -18px;', 'height: 46px; margin: auto -44px -30px;', opt=True)
r1('<div style="flex-grow: 1; padding: 18px 18px 18px; display: flex; flex-direction: column">', '<div style="flex-grow: 1; padding: 34px 44px 30px; display: flex; flex-direction: column">', opt=True)
r1('style="position: relative; margin-top: 34px; border: 1px solid var(--ac-dark-beige); padding: 0 16px 44px;', 'style="' + SMALL + 'position: relative; margin-top: 0; border: 1px solid var(--ac-dark-beige); padding: 0 16px 44px;', opt=True)
r1('style="position: relative; margin-top: 18px; border: 1px solid var(--ac-near-black); background: var(--ac-near-black); padding: 0 16px 18px;', 'style="' + SMALL + 'position: relative; margin-top: 0; border: 1px solid var(--ac-near-black); background: var(--ac-near-black); padding: 0 16px 18px;', opt=True)
r1('style="position: relative; margin-top: 34px; border: 1px solid var(--ac-near-black); background: var(--ac-near-black); padding: 0 16px 18px;', 'style="' + SMALL + 'position: relative; margin-top: 0; border: 1px solid var(--ac-near-black); background: var(--ac-near-black); padding: 0 16px 18px;', opt=True)
r1('style="margin-top: 18px; border: 1px solid var(--ac-dark-beige); padding: 0 16px 18px;', 'style="' + SMALL + 'margin-top: 0; border: 1px solid var(--ac-dark-beige); padding: 0 16px 18px;', opt=True)
r1('<article data-brunch-card="1" style="position: relative; margin-top: 34px;', '<article data-brunch-card="1" style="flex: 1 1 100%; max-width: 1118px; box-sizing: border-box; display: grid !important; grid-template-columns: 5fr 7fr; position: relative; margin-top: 0;', opt=True)
r1('<div style="position: relative; height: 150px; overflow: hidden"><img src="/_blob/913442a843da7607597400e3a1b5a982"', '<div style="position: relative; min-height: 300px; overflow: hidden"><img src="/_blob/913442a843da7607597400e3a1b5a982"', opt=True)
r1('alt="Brindis con cócteles junto a la piscina" style="width: 100%; height: 100%;', 'alt="Brindis con cócteles junto a la piscina" style="position: absolute; left: 0; top: 0; width: 100%; height: 100%;', opt=True)
r1('<div style="padding: 0 18px 20px; display: flex; flex-direction: column"><span style="align-self: flex-start; margin-top: -14px;', '<div style="padding: 34px 40px 30px; display: flex; flex-direction: column"><span style="align-self: flex-start; margin-top: 0;', opt=True)
d = d[:a] + '<div style="margin-top: 52px; display: flex; flex-wrap: wrap; justify-content: center; align-items: stretch; gap: 44px 28px">\n' + grid + '</div>\n' + d[b:]
s = s[:i] + d + s[j:]

# ---------- Cada semana: tres tarjetas a la vista ----------
rep('<section id="semana" style="position: relative; z-index: 0; padding: 48px 0 0;', '<section id="semana" style="position: relative; z-index: 0; padding: 96px 0 0;')
rep('Toca una tarjeta para ver qué incluye', 'Elige una tarjeta para ver qué incluye')
rep('<div style="display: flex; gap: 16px; padding: 26px 20px 14px; overflow-x: auto; overflow-y: hidden; overscroll-behavior-x: contain; scroll-snap-type: x mandatory" data-noscroll="true">',
    '<div style="display: flex; justify-content: center; gap: 36px; padding: 40px 40px 14px">')
rep('<div style="flex: 0 0 284px; height: 432px; scroll-snap-align: center;', '<div style="flex: 0 0 340px; height: 470px;', 3)
rep('<div style="position: relative; height: 200px; overflow: hidden">', '<div style="position: relative; height: 236px; overflow: hidden">', 3)
s = s.replace('style="width: 100%; height: 200px; object-fit: cover;', 'style="width: 100%; height: 236px; object-fit: cover;')

# ---------- San Silvestre ----------
if 'También corremos' in s:
    rep('<section id="comunidad" style="padding: 44px 20px 0;', '<section id="comunidad" style="padding: 96px 40px 0;')
    rep('<article style="margin-top: 22px; width: 100%; box-sizing: border-box; padding: 10px; background: var(--ac-white); box-shadow: var(--shadow-lg); transform: rotate(-1.5deg)">',
        '<article style="margin-top: 28px; width: 780px; box-sizing: border-box; padding: 12px; background: var(--ac-white); box-shadow: var(--shadow-lg); transform: rotate(-1.2deg)">')
    rep('padding: 26px 18px 0; display: flex; flex-direction: column; gap: 8px; min-height: 215px; box-sizing: border-box">', 'padding: 36px 32px 0; display: flex; flex-direction: column; gap: 10px; min-height: 270px; box-sizing: border-box">')
    rep('font-weight: 600; font-size: 34px; line-height: 34px; letter-spacing: -0.02em; text-transform: uppercase">San Silvestre del Caribe', 'font-weight: 600; font-size: 56px; line-height: 56px; letter-spacing: -0.02em; text-transform: uppercase">San Silvestre del Caribe')
    rep('<div style="font-weight: 600; font-size: 17px; line-height: 22px">Dom 27 de diciembre', '<div style="font-weight: 600; font-size: 21px; line-height: 28px">Dom 27 de diciembre')
    rep('<div style="margin: auto -18px 0; background: #14009A; color: var(--ac-white); padding: 14px 18px;', '<div style="margin: auto -32px 0; background: #14009A; color: var(--ac-white); padding: 16px 32px;')
elif 'data-race-card' in s:
    rep('<section id="comunidad" style="padding: 36px 12px 0">', '<section id="comunidad" style="padding: 72px 40px 0; display: flex; justify-content: center">')
    rep('<article data-race-card="1" style="position: relative;', '<article data-race-card="1" style="width: 900px; position: relative;')
    rep('padding: 22px 18px 26px; display: flex; flex-direction: column">', 'padding: 44px 48px 44px; display: grid; grid-template-columns: 1fr 260px; column-gap: 40px; align-content: start">')
    rep('<div aria-hidden="true" style="position: relative; align-self: center; margin-top: 20px; width: 236px;', '<div aria-hidden="true" style="position: relative; grid-column: 2; grid-row: 1 / span 3; align-self: center; margin-top: 0; width: 256px;')
    rep('font-weight: 700; font-size: 40px; line-height: 38px; letter-spacing: -0.02em; text-transform: uppercase">San Silvestre', 'font-weight: 700; font-size: 64px; line-height: 60px; letter-spacing: -0.02em; text-transform: uppercase">San Silvestre')
    rep('<div style="align-self: flex-start; padding: 5px 9px; background: #14009A;', '<div style="justify-self: start; align-self: flex-start; padding: 5px 9px; background: #14009A;')
    rep('<div style="padding: 4px 18px 0; display: flex; flex-direction: column">', '<div style="padding: 4px 48px 0; display: flex; flex-direction: column">')

# ---------- Empresas: foto grande y "Orden del día" superpuesta ----------
i, j = sec('<section id="empresas"', '</section>')
d = s[i:j]
def dr(x, y):
    global d
    assert d.count(x) == 1, x[:70]
    d = d.replace(x, y)
dr('<section id="empresas" style="position: relative; z-index: 0; margin: 48px 0 0; padding: 0 0 26px; display: flex; flex-direction: column">',
   '<section id="empresas" style="position: relative; z-index: 0; margin: 104px 40px 0; padding: 0; display: grid; grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); align-items: center">')
dr('<div data-bp-photo="1" style="position: relative; height: 300px; overflow: hidden">', '<div data-bp-photo="1" style="position: relative; height: 600px; overflow: hidden; grid-column: 1; grid-row: 2">')
dr('<div data-bp-head="1" style="padding: 0 20px 22px; text-align: center; color: #1C1C1C">', '<div data-bp-head="1" style="grid-column: 1 / -1; padding: 0 0 36px; text-align: center; color: #1C1C1C">')
dr("font-size: 36px; line-height: 38px; letter-spacing: 0.06em; text-transform: uppercase\">AC Business", "font-size: 58px; line-height: 60px; letter-spacing: 0.06em; text-transform: uppercase\">AC Business")
dr('<div data-bp-sheet="1" style="position: relative; margin: -64px 16px 0;', '<div data-bp-sheet="1" style="position: relative; grid-column: 2; grid-row: 2; margin: 0 0 0 -36px;')
dr('padding: 22px 20px 20px; display: flex; flex-direction: column; animation: acRise', 'padding: 32px 34px 28px; display: flex; flex-direction: column; animation: acRise')
dr('style="margin: 10px 20px 0; display: inline-flex; align-items: center; min-height: 44px; align-self: center;', 'style="grid-column: 1 / -1; margin: 18px 0 0; display: inline-flex; align-items: center; min-height: 44px; justify-self: center;')
s = s[:i] + d + s[j:]

# ---------- Alrededores: categorías a la izquierda, lista a la derecha ----------
i, j = sec('<section id="llegar"', '</section>')
d = s[i:j]
d = d.replace('padding: 44px 20px 0; display: flex; flex-direction: column">', 'padding: 96px 40px 0; display: flex; flex-direction: column">')
map_a = d.index('<a href="https://www.google.com/maps/place/')
title_a = d.index('<div style="margin-top: 14px; font-family: var(--font-display); font-size: 10px; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ac-dark-beige)">{{zona.title}}</div>')
left = d[map_a:title_a]
right = d[title_a:-len('</section>')]
left = left.replace('<span style="display: block; height: 290px;', '<span style="display: block; height: 440px;')
left = left.replace('style="margin-top: 20px; border: 1px solid var(--ac-dark-beige); padding: 8px;', 'style="margin-top: 0; border: 1px solid var(--ac-dark-beige); padding: 10px;')
left = left.replace('style="margin-top: 16px; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 4px"', 'style="margin-top: 20px; display: grid; grid-template-columns: minmax(0, 1fr); gap: 6px"')
left = left.replace('style="min-height: 48px; padding: 3px 2px; border: 1px solid var(--ac-dark-beige);', 'style="min-height: 50px; padding: 3px 18px; text-align: left; border: 1px solid var(--ac-dark-beige);')
left = left.replace('font-size: clamp(9px, 2.7vw, 10.5px); font-weight: 600; letter-spacing: 0;', 'font-size: 12px; font-weight: 600; letter-spacing: 0.12em;')
right = right.replace('<div style="margin-top: 14px; font-family: var(--font-display)', '<div style="margin-top: 0; font-family: var(--font-display)', 1)
assert 'text-align: left; border' in left and 'letter-spacing: 0.12em' in left and 'minmax(0, 1fr); gap: 6px' in left
d = (d[:map_a] + '<div style="margin-top: 44px; display: grid; grid-template-columns: 540px minmax(0, 1fr); column-gap: 56px; align-items: start">\n'
     '<div style="display: flex; flex-direction: column">\n' + left + '</div>\n<div style="display: flex; flex-direction: column">\n' + right + '</div>\n</div>\n</section>')
s = s[:i] + d + s[j:]
rep('display: flex; flex-direction: column; padding: 0 0 28px">', 'display: flex; flex-direction: column; padding: 0 0 72px">')

# ---------- Estadía ----------
rep('margin-top: 26px; background: var(--ac-slate); color: var(--ac-white); padding: 20px 24px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 18px">',
    'margin-top: 64px; background: var(--ac-slate); color: var(--ac-white); padding: 64px 80px; display: flex; flex-direction: row; justify-content: center; align-items: center; text-align: center; gap: 72px">')
s = s.replace("font-size: 30px; line-height: 36px; letter-spacing: 0.1em; text-transform: uppercase", "font-size: 38px; line-height: 46px; letter-spacing: 0.1em; white-space: nowrap; text-transform: uppercase")
rep('<div style="align-self: stretch; display: flex; flex-direction: column; gap: 10px; text-align: left"><div style="font-family: var(--font-display); font-size: 10px; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ac-white); text-align: center">Nuestras habitaciones',
    '<div style="width: 420px; display: flex; flex-direction: column; gap: 10px; text-align: left"><div style="font-family: var(--font-display); font-size: 10px; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ac-white); text-align: center">Nuestras habitaciones')
rep('style="align-self: stretch; display: flex; align-items: center; justify-content: center; min-height: 54px; background: #FBF8F4; color: var(--ac-near-black);',
    'style="flex-shrink: 0; padding: 0 36px; display: flex; align-items: center; justify-content: center; min-height: 58px; background: #FBF8F4; color: var(--ac-near-black);')

# ---------- pie ----------
rep('<div style="flex-grow: 1; margin: 14px; border: 1px solid rgba(255,255,255,0.45);', '<div style="flex-grow: 1; align-self: center; width: 1200px; box-sizing: border-box; margin: 22px 0; border: 1px solid rgba(255,255,255,0.45);')
rep('padding: 24px 20px 18px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 14px">', 'padding: 44px 56px 24px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 18px">')
rep('gap: 18px; width: 100%; text-align: left">', 'gap: 56px; width: 640px; text-align: left">')
rep("font-style: italic; font-size: 22px; line-height: 28px\">Te esperamos", "font-style: italic; font-size: 28px; line-height: 34px\">Te esperamos")

open(S + '/canvas/project/Desktop%s.dc.html' % _sfx, 'w', encoding='utf-8').write(s)
print('ok', len(s))

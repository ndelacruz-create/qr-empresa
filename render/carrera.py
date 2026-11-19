import re, os
S = os.environ.get('KIT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=open(S+'/canvas/project/V2-navidad.dc.html',encoding='utf-8').read()
IND,MAG,PUR,PINK,W='#14009A','#B43695','#6C3FD1','#FF9BD6','#FFFFFF'
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
# ---- portada: banderines y meta a cuadros ----
def pennants(w=300,n=13):
    out=['<svg aria-hidden="true" width="%d" height="30" viewBox="0 0 %d 30" style="position: absolute; left: 50%%; top: 0; transform: translateX(-50%%); overflow: visible; pointer-events: none"><path d="M0 2 Q%d 18 %d 2" stroke="%s" stroke-width="1" fill="none"/>'%(w,w,w//2,w,PINK)]
    cols=[MAG,W,PUR]
    for i in range(n):
        x=10+i*(w-20)/(n-1); t=x/w; y=2+(1-(2*t-1)**2)*8
        out.append('<g style="transform-box: fill-box; transform-origin: 50%% 0; animation: acFlag %.1fs %.2fs ease-in-out infinite alternate"><path d="M%.1f %.1f l7 0 l-3.5 11z" fill="%s"/></g>'%((2.0,2.4,2.8)[i%3],(i%5)*0.3,x-3.5,y,cols[i%3]))
    out.append('</svg>'); return ''.join(out)
CHECK='repeating-conic-gradient('+IND+' 0 25%, '+W+' 0 50%) 0 0 / 10px 10px'
i=s.index('<sc-if value="{{agenda.fest}}"'); j=s.index('</sc-if>',i)+8
s=s[:i]+'<sc-if value="{{agenda.fest}}" hint-placeholder-val="{{true}}">'+pennants()+'</sc-if>'+s[j:]
i=s.index('<sc-if value="{{agenda.fest}}"',i+40); j=s.index('</sc-if>',i)+8
s=s[:i]+'<sc-if value="{{agenda.fest}}" hint-placeholder-val="{{true}}"><span aria-hidden="true" style="position: absolute; left: 0; right: 0; bottom: 0; height: 10px; background: '+CHECK+'"></span></sc-if>'+s[j:]
rep(" { y: 2026, m: 12, d: 24, name: 'Cena de Nochebuena', href: '#temporada' },\n","")
k=s.index('var isFest'); e=s.index('\n',s.index('var agenda',k)); line=s[k:e]
line=line.replace("nx.name === 'Cena de Nochebuena'","nx.name === 'San Silvestre del Caribe'").replace("name1: isFest ? 'Cena de ' : nx.name","name1: isFest ? 'San Silvestre ' : nx.name").replace("name2: isFest ? 'Nochebuena' : ''","name2: isFest ? 'del Caribe' : ''")
line=line.replace("'#FBF6EC'","'"+IND+"'").replace("'2px solid #1E4D3A'","'0'").replace("'#1E2B24'","'"+W+"'").replace("eyebrow: isFest ? '#A3262E'","eyebrow: isFest ? '"+PINK+"'").replace("accent: '#A3262E'","accent: isFest ? '"+PINK+"' : '#A3262E'")
assert 'Nochebuena' not in line, line; s=s[:k]+line+s[e:]
# ---- Temporada: sale Nochebuena ----
i=s.index('<sc-if value="{{showNoche}}"'); j=s.index('</sc-if>',s.index('</article>',i))+8; s=s[:i]+s[j:]
# ---- quitar la sección vieja de la carrera ----
i=s.index('<sc-if value="{{showSS}}"'); j=s.index('</sc-if>',s.index('</section>',i))+8; s=s[:i]+s[j:]
# ---- tarjeta grande de la carrera bajo la portada ----
PIN='<span style="position: absolute; width: 7px; height: 7px; border-radius: 50%; background: #C9C9D6; box-shadow: inset 0 1px 1px rgba(0,0,0,0.35); {p}"></span>'
BIB=('<div aria-hidden="true" style="position: relative; align-self: center; margin-top: 20px; width: 236px; background: '+W+'; color: '+IND+'; padding: 12px 16px 12px; box-sizing: border-box; box-shadow: 0 10px 24px rgba(10,0,80,0.35); transform: rotate(-3deg); transform-origin: 50% 0; animation: acBib 4s ease-in-out infinite alternate; text-align: center">'
 +PIN.format(p='left: 8px; top: 8px')+PIN.format(p='right: 8px; top: 8px')+PIN.format(p='left: 8px; bottom: 8px')+PIN.format(p='right: 8px; bottom: 8px')+
 '<div style="background: '+MAG+'; color: '+W+'; margin: 6px 6px 0; padding: 4px 0; font-family: var(--font-display); font-size: 8px; font-weight: 600; letter-spacing: 0.12em; white-space: nowrap; text-transform: uppercase">San Silvestre del Caribe 2026</div>'
 '<div style="font-family: var(--font-display); font-weight: 700; font-size: 84px; line-height: 84px; letter-spacing: -0.04em; margin-top: 4px">27</div>'
 '<div style="font-family: var(--font-display); font-weight: 600; font-size: 12px; letter-spacing: 0.26em; text-transform: uppercase">Dic · 5K · 10K</div></div>')
RUN=('<div aria-hidden="true" style="position: relative; height: 52px; margin-top: 22px; container-type: inline-size; pointer-events: none">'
 '<div style="position: absolute; left: 6px; right: 6px; top: 14px; height: 2px; background: rgba(255,255,255,0.22)"></div>'
 '<div style="position: absolute; left: 6px; right: 6px; top: 14px; height: 2px; background: linear-gradient(90deg, '+MAG+', '+PINK+'); transform-origin: 0 50%; animation: acRoute 6s cubic-bezier(.45,.05,.55,.95) infinite"></div>'
 '<span style="position: absolute; left: 6px; top: 9px; width: 12px; height: 12px; margin-left: -6px; border-radius: 50%; background: '+W+'; box-shadow: 0 0 0 4px rgba(255,155,214,0.35), 0 0 14px rgba(255,155,214,0.9); animation: acRouteDot 6s cubic-bezier(.45,.05,.55,.95) infinite"></span>'
 + ''.join('<span style="position: absolute; left: %s; top: 10px; width: 2px; height: 10px; background: rgba(255,255,255,0.6)"></span><span style="position: absolute; left: %s; top: 30px; transform: translateX(%s); white-space: nowrap; font-family: var(--font-display); font-size: 9px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: rgba(255,255,255,0.8)">%s</span>' % (x, x, tx, t) for x, tx, t in (('6px','0','Salida'), ('50%','-50%','5K'), ('calc(100% - 8px)','-100%','10K')))
 + '</div>')
KIT=('<div style="margin-top: 18px; display: flex; gap: 12px; align-items: flex-start; padding: 14px; border: 1px solid rgba(255,255,255,0.35)">'
 '<svg aria-hidden="true" width="26" height="26" viewBox="0 0 26 26" fill="none" stroke="'+PINK+'" stroke-width="1.6" stroke-linejoin="round" style="flex-shrink: 0"><path d="M4 9h18l-1.5 14h-15z"/><path d="M9 9V6.5a4 4 0 0 1 8 0V9"/></svg>'
 '<div style="display: flex; flex-direction: column; gap: 3px"><span style="font-family: var(--font-display); font-weight: 600; font-size: 15px; line-height: 20px">Recoge tu kit en AC Hotel</span>'
 '<span style="font-size: 13px; line-height: 19px; color: rgba(255,255,255,0.85)">Sábado 26 de diciembre, un día antes de la carrera.</span></div></div>')
SEC=('<sc-if value="{{showSS}}" hint-placeholder-val="{{true}}">\n<section id="comunidad" style="padding: 36px 12px 0">\n'
'<article data-race-card="1" style="position: relative; overflow: hidden; background: '+IND+'; color: '+W+'; box-shadow: var(--shadow-lg); animation: acRise 0.9s ease-out both">\n'
'<div style="background: repeating-conic-gradient(from 0deg at 50% 80%, '+MAG+' 0deg 10deg, '+PUR+' 10deg 20deg); padding: 22px 18px 26px; display: flex; flex-direction: column">'
'<div style="align-self: flex-start; padding: 5px 9px; background: '+IND+'; font-family: var(--font-display); font-size: 10px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase">Patrocinador oficial · 5ª edición</div>'
'<h2 style="margin: 14px 0 0; font-family: var(--font-display); font-weight: 700; font-size: 40px; line-height: 38px; letter-spacing: -0.02em; text-transform: uppercase">San Silvestre<br>del Caribe</h2>'
'<div style="margin-top: 10px; font-weight: 600; font-size: 16px; line-height: 22px">Dom 27 de diciembre · {{ cdSS }}</div>'
+BIB+'</div>\n'
'<div style="padding: 4px 18px 0; display: flex; flex-direction: column">'+RUN+KIT+
'<div style="margin-top: 12px; font-size: 13px; line-height: 19px; color: rgba(255,255,255,0.85)">5K y 10K · Organiza Punta Cana Running</div>'
'<a href="https://web.rockthesport.com/es/event/san-silvestre-del-caribe-2026" target="_blank" rel="noopener noreferrer" style="margin: 16px 0 22px; display: flex; align-items: center; justify-content: center; min-height: 52px; background: '+W+'; color: '+IND+'; font-family: var(--font-display); font-weight: 700; font-size: 13px; letter-spacing: 0.14em; text-transform: uppercase; text-decoration: none">Inscribirme →</a></div>\n'
'<div aria-hidden="true" style="height: 12px; background: '+CHECK+'"></div>\n'
'</article>\n</section>\n</sc-if>\n\n')
i=s.index('<nav aria-label="Ir a una sección"'); j=s.index('</nav>',i)+6
s=s[:j]+'\n\n'+SEC+s[j:]
rep("cdNoche: cd(2026, 12, 24),","cdNoche: cd(2026, 12, 24), cdSS: cd(2026, 12, 27),")
KF="@keyframes acRoute{0%{transform:scaleX(0);opacity:1}80%{transform:scaleX(1);opacity:1}100%{transform:scaleX(1);opacity:0}}@keyframes acRouteDot{0%{transform:translateX(0);opacity:1}80%{transform:translateX(calc(100cqw - 12px));opacity:1}100%{transform:translateX(calc(100cqw - 12px));opacity:0}}@keyframes acBib{from{transform:rotate(-3deg)}to{transform:rotate(-1deg)}}"
s=s.replace('</style>',KF+'</style>',1)
assert 'Nochebuena' not in re.sub(r'<script.*?</script>','',s,flags=re.S).replace('cdNoche',''), 'quedó Nochebuena'
open(S+'/canvas/project/V2-carrera.dc.html','w',encoding='utf-8').write(s); print('ok')

# ===================== Fin de Año destacada y Brunch mediano =====================
s=open(S+'/canvas/project/V2-carrera.dc.html',encoding='utf-8').read()
BLK,GOLD,CHAMP,CRM='#161514','#C9A24A','#E9D8A6','#F6EFE2'
DECO='repeating-linear-gradient(135deg, '+GOLD+' 0 4px, '+BLK+' 4px 9px)'
STRIP='<div aria-hidden="true" style="height: 14px; background: '+DECO+'"></div>'
STAR4='M0 -6 C0.8 -1.4 1.4 -0.8 6 0 C1.4 0.8 0.8 1.4 0 6 C-0.8 1.4 -1.4 0.8 -6 0 C-1.4 -0.8 -0.8 -1.4 0 -6Z'
TW=''.join('<svg aria-hidden="true" width="18" height="18" viewBox="-9 -9 18 18" style="position: absolute; left: %s; top: %s; overflow: visible; animation: acTwinkle %.1fs %.1fs ease-in-out infinite"><path d="%s" fill="%s" transform="scale(%s)"/></svg>'%(x,y,d,dl,STAR4,c,sc) for x,y,d,dl,c,sc in (('12%','14%',2.4,0,CHAMP,1.2),('30%','8%',3.0,0.8,W,0.8),('58%','18%',2.6,1.4,CHAMP,1),('80%','10%',3.2,0.4,W,1.3),('70%','40%',2.8,2.0,CHAMP,0.7)))
SEALF=('<div aria-hidden="true" style="position: absolute; right: 8px; top: 118px; z-index: 1; width: 104px; height: 104px; transform: rotate(-6deg); filter: drop-shadow(0 3px 8px rgba(0,0,0,0.45))">'
 '<svg width="104" height="104" viewBox="0 0 104 104" style="display: block">'
 '<defs><path id="fySealRim" d="M52 52 m-38 0 a38 38 0 1 1 76 0 a38 38 0 1 1 -76 0"/></defs>'
 '<circle cx="52" cy="52" r="51" fill="'+GOLD+'"/><circle cx="52" cy="52" r="47.5" fill="none" stroke="'+BLK+'" stroke-width="1"/><circle cx="52" cy="52" r="28.5" fill="none" stroke="'+BLK+'" stroke-width="1"/>'
 '<g style="transform-box: view-box; transform-origin: 52px 52px; animation: acSpin 36s linear infinite"><text fill="'+BLK+'" style="font-family: Montserrat, sans-serif; font-size: 8.2px; font-weight: 700; letter-spacing: 0.16em"><textPath href="#fySealRim" textLength="232" lengthAdjust="spacing">PREVENTA ✦ OPEN BAR ✦ ORQUESTA EN VIVO ✦</textPath></text></g>'
 '<text x="52" y="61" text-anchor="middle" fill="'+BLK+'" style="font-family: \'Cormorant Garamond\', serif; font-style: italic; font-weight: 700; font-size: 24px">2027</text></svg></div>')
BTNS='display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; text-decoration: none'
ITEMS=['Orquesta en vivo','Trago de bienvenida','1 botella de vino por mesa','Estación de buffet','Open bar','Cotillones','Ritual de las 12 uvas','Conteo regresivo','Fuegos artificiales fríos']
LIST=('<ul style="margin: 16px 0 0; padding: 14px 0 0; border-top: 1px solid rgba(201,162,74,0.5); list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 7px 14px; font-size: 13.5px; line-height: 18px; color: '+CRM+'">'
 +''.join('<li style="display: flex; gap: 7px; align-items: baseline"><svg aria-hidden="true" width="8" height="8" viewBox="-6 -6 12 12" style="flex-shrink: 0"><path d="'+STAR4+'" fill="'+GOLD+'"/></svg><span>'+t+'</span></li>' for t in ITEMS)+'</ul>')
CALF=('https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=Gran+Cena+de+Fin+de+A%C3%B1o+en+AC+Hotel+Punta+Cana&amp;dates=20261231T230000Z/20270101T040000Z'
      '&amp;location=AC+Hotel+Punta+Cana,+Av.+Barcel%C3%B3+Km+9,+B%C3%A1varo&amp;details=Orquesta+en+vivo,+open+bar+y+fuegos+artificiales+fr%C3%ADos.+Reserva+por+WhatsApp.')
FIN=('<sc-if value="{{showFin}}" hint-placeholder-val="{{true}}">\n'
'<article data-fest-card="1" style="position: relative; margin-top: 36px; background: '+BLK+'; border: 2px solid '+GOLD+'; color: '+CRM+'; overflow: hidden; display: flex; flex-direction: column; animation: acRise 0.9s ease-out both">\n'+STRIP+'\n'
'<div style="position: relative; height: 176px; overflow: hidden; margin: 14px 14px 0; border: 1px solid '+GOLD+'"><img src="/_blob/5afe661ac36a6e9b2d608f682e37d278" alt="Brindis con luces de bengala" style="width: 100%; height: 100%; object-fit: cover; display: block; animation: acZoom 10s ease-out both">'+TW+'</div>\n'+SEALF+'\n'
'<div style="flex-grow: 1; padding: 18px 18px 18px; display: flex; flex-direction: column">\n'
'<div style="align-self: flex-start; background: '+GOLD+'; color: '+BLK+'; padding: 7px 10px; font-family: var(--font-display); font-size: 9.5px; font-weight: 600; letter-spacing: 0.13em; text-transform: uppercase; white-space: nowrap">Jue 31 dic · 7:00 pm · {{ cdFin }}</div>\n'
'<h3 style="margin: 14px 0 0; display: flex; flex-direction: column; max-width: calc(100% - 84px)"><span style="font-family: \'Cormorant Garamond\', serif; font-weight: 500; font-size: 26px; line-height: 28px; color: '+CRM+'">Gran Cena de</span><span style="font-family: \'Cormorant Garamond\', serif; font-style: italic; font-weight: 600; font-size: 44px; line-height: 46px; color: '+CHAMP+'">Fin de Año</span></h3>\n'
'<p style="margin: 10px 0 0; font-family: \'Cormorant Garamond\', serif; font-style: italic; font-size: 20px; line-height: 25px; color: '+CRM+'">Despide el año con una noche inolvidable.</p>\n'+LIST+'\n'
'<div style="margin-top: 16px; padding: 12px 14px; border: 1px solid rgba(201,162,74,0.55); display: flex; flex-direction: column; gap: 4px">'
'<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 8px"><span style="font-family: var(--font-display); font-size: 10px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: '+GOLD+'">Preventa</span><span style="font-family: var(--font-display); font-weight: 700; font-size: 20px; color: '+CHAMP+'">US$120 <span style="font-size: 13px; font-weight: 600">+ imp.</span></span></div>'
'<div style="font-size: 12px; line-height: 17px; color: rgba(246,239,226,0.8)">Precio por persona. Infantes de 0 a 6 años, gratis.</div></div>\n'
'<a href="https://wa.link/hwnaf7" target="_blank" rel="noopener noreferrer" style="margin-top: 18px; min-height: 52px; background: '+GOLD+'; color: '+BLK+'; font-size: 12px; '+BTNS+'">Escríbenos para asistir</a>\n'
'<a href="'+CALF+'" target="_blank" rel="noopener noreferrer" style="margin-top: 10px; min-height: 44px; border: 1px solid '+CHAMP+'; color: '+CHAMP+'; font-size: 11px; '+BTNS+'">Guárdalo en tu calendario</a>\n'
'</div>\n'+STRIP.replace('"></div>','; transform: scaleY(-1)"></div>')+'\n</article>\n</sc-if>')
i=s.index('<sc-if value="{{showFin}}"'); j=s.index('</sc-if>',s.index('</a>',i))+8; s=s[:i]+FIN+s[j:]
BR=('<sc-if value="{{showBrunch}}" hint-placeholder-val="{{true}}">\n'
'<article data-brunch-card="1" style="position: relative; margin-top: 34px; background: #FBF8F4; border: 1px solid var(--ac-dark-beige); display: flex; flex-direction: column; color: var(--text-primary)">\n'
'<div style="position: relative; height: 150px; overflow: hidden"><img src="/_blob/5c1e8edad722490adac45253bcf680fb" alt="Estación de buffet del brunch" style="width: 100%; height: 100%; object-fit: cover; display: block"></div>\n'
'<div style="padding: 0 18px 20px; display: flex; flex-direction: column">'
'<span style="align-self: flex-start; margin-top: -14px; position: relative; background: #FBF8F4; border: 1px solid var(--ac-dark-beige); padding: 5px 12px; font-family: var(--font-display); font-size: 10px; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ac-dark-beige)">Vie 1 ene · desde la 1:00 pm</span>'
'<h3 style="margin: 12px 0 0; font-family: \'Cormorant Garamond\', serif; font-weight: 500; font-size: 28px; line-height: 31px">Brunch de Bienvenida <span style="font-style: italic; color: var(--ac-dark-beige)">2027</span></h3>'
'<p style="margin: 6px 0 0; font-family: \'Cormorant Garamond\', serif; font-style: italic; font-size: 18px; line-height: 23px; color: var(--text-secondary)">Comienza el año celebrando en familia.</p>'
'<p style="margin: 10px 0 0; font-size: 13.5px; line-height: 20px">DJ en vivo · Estación de buffet · Trago de bienvenida · Open bar de cervezas y bebidas sin alcohol</p>'
'<div style="margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px 16px; font-family: var(--font-display); font-size: 13px; font-weight: 600; color: var(--ac-dark-beige)"><span>Adultos US$50 + imp.</span><span>Niños 6–15 US$25 + imp.</span><span>0–6 años gratis</span></div>'
'<a href="https://wa.link/hwnaf7" target="_blank" rel="noopener noreferrer" style="margin-top: 16px; min-height: 46px; border: 1px solid var(--text-primary); color: var(--text-primary); font-size: 11px; '+BTNS+'">Escríbenos para asistir</a></div>\n'
'</article>\n</sc-if>')
i=s.index('<sc-if value="{{showBrunch}}"'); j=s.index('</sc-if>',s.index('</a>',i))+8; s=s[:i]+BR+s[j:]
s=s.replace("cdSS: cd(2026, 12, 27),","cdSS: cd(2026, 12, 27), cdFin: cd(2026, 12, 31),",1)
s=s.replace('</style>','@keyframes acTwinkle{0%,100%{opacity:0.15;transform:scale(0.6)}50%{opacity:1;transform:scale(1)}}</style>',1)
open(S+'/canvas/project/V2-carrera.dc.html','w',encoding='utf-8').write(s); print('fin ok')

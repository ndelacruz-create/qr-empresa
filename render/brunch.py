import re, os, math
S = os.environ.get('KIT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=open(S+'/canvas/project/V2-findeano.dc.html',encoding='utf-8').read()
CRM,INK,GOLD,TEAL,BLUSH,W='#FBF6EC','#2A2420','#B8892B','#2F6F73','#E9A88F','#FFFFFF'
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
CONF='repeating-linear-gradient(90deg, '+GOLD+' 0 10px, '+TEAL+' 10px 20px, '+BLUSH+' 20px 30px, '+CRM+' 30px 34px)'
def confetti(w=300,n=16):
    out=['<svg aria-hidden="true" width="%d" height="40" viewBox="0 0 %d 40" style="position: absolute; left: 50%%; top: 0; transform: translateX(-50%%); overflow: visible; pointer-events: none">'%(w,w)]
    cols=[GOLD,TEAL,BLUSH]
    for i in range(n):
        x=8+i*(w-16)/(n-1); dl=(i*0.37)%2.6; dur=(2.8,3.4,3.0,3.8)[i%4]
        shape='<rect x="-2.5" y="-1.2" width="5" height="2.4" rx="0.6" fill="%s"/>'%cols[i%3] if i%2 else '<circle r="1.8" fill="%s"/>'%cols[i%3]
        out.append('<g transform="translate(%.1f 0)"><g style="transform-box: fill-box; transform-origin: center; animation: acConf %.1fs %.2fs linear infinite; opacity: 0">%s</g></g>'%(x,dur,dl,shape))
    out.append('</svg>'); return ''.join(out)
i=s.index('<sc-if value="{{agenda.fest}}"'); j=s.index('</sc-if>',i)+8
s=s[:i]+'<sc-if value="{{agenda.fest}}" hint-placeholder-val="{{true}}">'+confetti()+'</sc-if>'+s[j:]
i=s.index('<sc-if value="{{agenda.fest}}"',i+40); j=s.index('</sc-if>',i)+8
s=s[:i]+'<sc-if value="{{agenda.fest}}" hint-placeholder-val="{{true}}"><span aria-hidden="true" style="position: absolute; left: 0; right: 0; bottom: 0; height: 8px; background: '+CONF+'"></span></sc-if>'+s[j:]
rep(" { y: 2026, m: 12, d: 31, name: 'Gran Cena de Fin de Año', href: '#temporada' },\n","")
k=s.index('var isFest'); e=s.index('\n',s.index('var agenda',k)); line=s[k:e]
for a,b in [("nx.name === 'Gran Cena de Fin de Año'","nx.name === 'Brunch de Bienvenida 2027'"),("name1: isFest ? 'Gran Cena de ' : nx.name","name1: isFest ? 'Brunch de Bienvenida ' : nx.name"),
            ("name2: isFest ? 'Fin de Año' : ''","name2: isFest ? '2027' : ''"),("bg: isFest ? '#161514'","bg: isFest ? '"+CRM+"'"),("ink: isFest ? '#F6EFE2'","ink: isFest ? '"+INK+"'"),
            ("eyebrow: isFest ? '#C9A24A'","eyebrow: isFest ? '"+TEAL+"'"),("accent: isFest ? '#E9D8A6'","accent: isFest ? '"+GOLD+"'"),("border: isFest ? '1px solid #C9A24A'","border: isFest ? '1px solid "+GOLD+"'")]:
    assert line.count(a)>=1,(a,line); line=line.replace(a,b)
s=s[:k]+line+s[e:]
# Temporada: sale Fin de Año; el Brunch pasa a destacado
i=s.index('<sc-if value="{{showFin}}"'); j=s.index('</sc-if>',s.index('</article>',i))+8; s=s[:i]+s[j:]
STRIP='<div aria-hidden="true" style="height: 14px; background: '+CONF+'"></div>'
def confrain():
    cols=[GOLD,TEAL,BLUSH,W]; out=[]
    for i in range(18):
        x=4+(i*37)%96; dl=(i*0.53)%4; dur=(3.6,4.4,4.0,5.0)[i%4]
        shp='<rect x="-3" y="-1.4" width="6" height="2.8" rx="0.7" fill="%s"/>'%cols[i%4] if i%3 else '<circle r="2.1" fill="%s"/>'%cols[i%4]
        out.append('<svg aria-hidden="true" width="10" height="10" viewBox="-5 -5 10 10" style="position: absolute; left: %d%%; top: -12px; overflow: visible; animation: acRain %.1fs %.2fs linear infinite; opacity: 0">%s</svg>'%(x,dur,dl,shp))
    return ''.join(out)
SEALB=('<div aria-hidden="true" style="position: absolute; left: 8px; top: 108px; z-index: 1; width: 104px; height: 104px; transform: rotate(6deg); filter: drop-shadow(0 3px 6px rgba(42,36,32,0.3))">'
 '<svg width="104" height="104" viewBox="0 0 104 104" style="display: block">'
 '<defs><path id="brSealRim" d="M52 52 m-38 0 a38 38 0 1 1 76 0 a38 38 0 1 1 -76 0"/></defs>'
 '<circle cx="52" cy="52" r="51" fill="'+TEAL+'"/><circle cx="52" cy="52" r="47.5" fill="none" stroke="'+GOLD+'" stroke-width="1"/><circle cx="52" cy="52" r="28.5" fill="none" stroke="'+GOLD+'" stroke-width="1"/>'
 '<g style="transform-box: view-box; transform-origin: 52px 52px; animation: acSpin 36s linear infinite"><text fill="'+CRM+'" style="font-family: Montserrat, sans-serif; font-size: 8.4px; font-weight: 600; letter-spacing: 0.16em"><textPath href="#brSealRim" textLength="232" lengthAdjust="spacing">DJ EN VIVO ✦ BUFFET ✦ BAR DE CERVEZAS ✦</textPath></text></g>'
 '<text x="52" y="61" text-anchor="middle" fill="'+CRM+'" style="font-family: \'Cormorant Garamond\', serif; font-style: italic; font-weight: 700; font-size: 24px">2027</text></svg></div>')
BTN='display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; text-decoration: none'
ITEMS=['DJ en vivo','Estación de buffet','Trago de bienvenida','Ambiente familiar y festivo','Open bar de cervezas y bebidas sin alcohol']
LIST=('<ul style="margin: 16px 0 0; padding: 14px 0 0; border-top: 2px dotted '+GOLD+'; list-style: none; display: flex; flex-direction: column; gap: 5px; font-family: \'Cormorant Garamond\', serif; font-size: 19px; line-height: 24px; color: '+INK+'">'
 +''.join('<li style="display: flex; align-items: baseline; gap: 10px"><svg aria-hidden="true" width="10" height="10" viewBox="0 0 10 10" style="flex-shrink: 0; position: relative; top: 1px"><circle cx="5" cy="5" r="4" fill="%s"/></svg><span>%s</span></li>'%([TEAL,GOLD,BLUSH][n%3],t) for n,t in enumerate(ITEMS))+'</ul>')
PRICE=lambda a,b:('<div style="display: flex; align-items: baseline; gap: 8px"><span style="font-family: \'Cormorant Garamond\', serif; font-size: 20px">%s</span><span aria-hidden="true" style="flex-grow: 1; border-bottom: 1px dotted '+TEAL+'"></span><span style="font-weight: 600; letter-spacing: 0.02em; font-family: var(--font-display); font-size: 14px; color: '+TEAL+'">%s</span></div>')%(a,b)
CAL=('https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=Brunch+de+Bienvenida+2027+en+AC+Hotel+Punta+Cana&amp;dates=20270101T170000Z/20270101T210000Z'
     '&amp;location=AC+Hotel+Punta+Cana,+Av.+Barcel%C3%B3+Km+9,+B%C3%A1varo&amp;details=DJ+en+vivo,+estaci%C3%B3n+de+buffet+y+open+bar+de+cervezas+y+bebidas+sin+alcohol.+Reserva+por+WhatsApp.')
BR=('<sc-if value="{{showBrunch}}" hint-placeholder-val="{{true}}">\n'
'<article data-fest-card="1" style="position: relative; margin-top: 36px; background: '+CRM+'; border: 2px solid '+GOLD+'; color: '+INK+'; overflow: hidden; display: flex; flex-direction: column; animation: acRise 0.9s ease-out both">\n'+STRIP+'\n'
'<div style="position: relative; height: 176px; overflow: hidden; margin: 14px 14px 0; border: 1px solid '+GOLD+'"><img src="/_blob/913442a843da7607597400e3a1b5a982" alt="Brindis con cócteles junto a la piscina" style="width: 100%; height: 100%; object-fit: cover; display: block; animation: acZoom 10s ease-out both">'+confrain()+'</div>\n'+SEALB+'\n'
'<div style="flex-grow: 1; padding: 18px 18px 18px; display: flex; flex-direction: column">\n'
'<div style="align-self: flex-start; background: '+TEAL+'; color: '+CRM+'; padding: 7px 10px; font-family: var(--font-display); font-size: 9.5px; font-weight: 600; letter-spacing: 0.13em; text-transform: uppercase; white-space: nowrap">Vie 1 ene · 1:00 pm · {{ cdBrunch }}</div>\n'
'<h3 style="margin: 14px 0 0; display: flex; flex-direction: column"><span style="font-family: \'Cormorant Garamond\', serif; font-weight: 500; font-size: 26px; line-height: 28px; color: '+INK+'">Brunch de Bienvenida</span><span style="font-family: \'Cormorant Garamond\', serif; font-style: italic; font-weight: 600; font-size: 44px; line-height: 46px; color: '+GOLD+'">al año 2027</span></h3>\n'
'<p style="margin: 10px 0 0; font-family: \'Cormorant Garamond\', serif; font-style: italic; font-size: 20px; line-height: 25px; color: '+INK+'">Comienza el año celebrando en familia.</p>\n'+LIST+'\n'
'<div style="margin-top: 16px; padding: 12px 14px; background: #F1EADB; display: flex; flex-direction: column; gap: 4px">'+PRICE('Adultos','US$50 + imp.')+PRICE('Niños 6 a 15','US$25 + imp.')+PRICE('Infantes 0 a 6','Gratis')+
'<div style="margin-top: 4px; font-size: 12px; line-height: 17px; color: #5A4E44">Precio por persona. Impuestos del 28%.</div></div>\n'
'<a href="https://wa.link/hwnaf7" target="_blank" rel="noopener noreferrer" style="margin-top: 18px; min-height: 52px; background: '+TEAL+'; color: '+CRM+'; font-size: 12px; '+BTN+'">Escríbenos para asistir</a>\n'
'<a href="'+CAL+'" target="_blank" rel="noopener noreferrer" style="margin-top: 10px; min-height: 44px; border: 1px solid '+INK+'; color: '+INK+'; font-size: 11px; '+BTN+'">Guárdalo en tu calendario</a>\n'
'</div>\n'+STRIP+'\n</article>\n</sc-if>')
i=s.index('<sc-if value="{{showBrunch}}"'); j=s.index('</sc-if>',s.index('</article>',i))+8; s=s[:i]+BR+s[j:]
rep("cdFin: cd(2026, 12, 31),","cdFin: cd(2026, 12, 31), cdBrunch: cd(2027, 1, 1),")
s=s.replace('</style>','@keyframes acConf{0%{opacity:0;transform:translateY(-6px) rotate(0)}10%{opacity:1}85%{opacity:1}100%{opacity:0;transform:translateY(34px) rotate(300deg)}}@keyframes acRain{0%{opacity:0;transform:translateY(0) rotate(0)}8%{opacity:1}90%{opacity:1}100%{opacity:0;transform:translateY(196px) rotate(420deg)}}</style>',1)
txt=re.sub(r'<script.*?</script>','',s,flags=re.S)
assert 'Fin de Año' not in txt and 'San Silvestre' not in txt, 'quedan eventos pasados'
open(S+'/canvas/project/V2-brunch.dc.html','w',encoding='utf-8').write(s); print('ok')

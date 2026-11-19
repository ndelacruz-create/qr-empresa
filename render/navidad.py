import re
S = os.environ.get('KIT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=open(S+'/canvas/project/V2.dc.html',encoding='utf-8').read()
RED,GREEN,GOLD,CREAM,INK,PINE='#A3262E','#1E4D3A','#C9A24A','#FBF6EC','#1E2B24','#2E6B4F'
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
PLAID=('repeating-linear-gradient(90deg, rgba(163,38,46,0.9) 0 5px, transparent 5px 13px), '
       'repeating-linear-gradient(0deg, rgba(201,162,74,0.8) 0 2px, transparent 2px 9px), '+GREEN)
def ornaments(w=300,n=11):
    out=['<svg aria-hidden="true" width="%d" height="40" viewBox="0 0 %d 40" style="position: absolute; left: 50%%; top: 0; transform: translateX(-50%%); overflow: visible; pointer-events: none"><path d="M0 2 Q%d 22 %d 2" stroke="%s" stroke-width="1.2" fill="none"/>'%(w,w,w//2,w,GREEN)]
    cols=[RED,GOLD,GREEN]
    for i in range(n):
        x=14+i*(w-28)/(n-1); t=x/w; y=2+(1-(2*t-1)**2)*10
        L=[8,13,10][i%3]; r=[5,4.2,5.5][i%3]
        star = i%4==3
        body = ('<path d="M0 %.1f l1.6 3.4 3.7 0.4 -2.8 2.5 0.8 3.7 -3.3 -1.9 -3.3 1.9 0.8 -3.7 -2.8 -2.5 3.7 -0.4z" fill="%s"/>'%(L, GOLD)) if star else \
               ('<rect x="-1.6" y="%.1f" width="3.2" height="2.4" fill="%s"/><circle cx="0" cy="%.1f" r="%.1f" fill="%s"/><path d="M-%.1f %.1f a%.1f %.1f 0 0 1 %.1f 0" stroke="%s" stroke-width="0.7" fill="none" opacity="0.6"/>'%(L-1,GOLD,L+1.4+r,r,cols[i%3],r*0.6,L+1.4+r-r*0.3,r*0.6,r*0.5,r*1.2,CREAM))
        out.append('<g style="transform-box: fill-box; transform-origin: 50%% 0; animation: acFlag %.1fs %.2fs ease-in-out infinite alternate"><g transform="translate(%.1f %.1f)"><path d="M0 0 V%d" stroke="%s" stroke-width="0.8"/>%s</g></g>'%((2.2,2.6,3.0)[i%3],(i%5)*0.3,x,y,L,GOLD,body))
    out.append('</svg>'); return ''.join(out)
# ---- portada ----
i=s.index('<sc-if value="{{agenda.fest}}"'); j=s.index('</sc-if>',i)+8
s=s[:i]+'<sc-if value="{{agenda.fest}}" hint-placeholder-val="{{true}}">'+ornaments()+'</sc-if>'+s[j:]
i=s.index('<sc-if value="{{agenda.fest}}"',i+40); j=s.index('</sc-if>',i)+8
s=s[:i]+'<sc-if value="{{agenda.fest}}" hint-placeholder-val="{{true}}"><span aria-hidden="true" style="position: absolute; left: 0; right: 0; bottom: 0; height: 10px; background: '+PLAID+'"></span></sc-if>'+s[j:]
rep(" { y: 2026, m: 11, d: 26, name: 'Cena de Thanksgiving', href: '#temporada' },\n","")
k=s.index('var isFest'); e=s.index('\n',s.index('var agenda',k))
line=s[k:e]
line=line.replace("nx.name === 'Cena de Thanksgiving'","nx.name === 'Cena de Nochebuena'").replace("'Thanksgiving'","'Nochebuena'")
line=line.replace("'#FBF3E4'","'"+CREAM+"'").replace("'2px solid #3B2418'","'2px solid "+GREEN+"'").replace("'#3B2418'","'"+INK+"'").replace("'#7A2833'","'"+RED+"'").replace("'#C0612B'","'"+RED+"'")
assert 'Thanksgiving' not in line; s=s[:k]+line+s[e:]
rep("var sT = left(2026, 11, 26) >= 0, ","var ")
rep("showThanks: sT, ",""); rep("noSeason: !(sT || ","noSeason: !(")
rep("cdThanks: cd(2026, 11, 26),","cdNoche: cd(2026, 12, 24),")
# ---- Temporada ----
i=s.index('<sc-if value="{{showThanks}}"'); j=s.index('<sc-if value="{{showNoche}}"'); s=s[:i]+s[j:]
i=s.index('<sc-if value="{{showNoche}}"'); j=s.index('</sc-if>',i)+8
STRIP='<div aria-hidden="true" style="height: 14px; background: '+PLAID+'"></div>'
STAR='M52 38 l4.1 8.4 9.3 1.3 -6.7 6.5 1.6 9.2 -8.3 -4.4 -8.3 4.4 1.6 -9.2 -6.7 -6.5 9.3 -1.3z'
SEAL=('<div aria-hidden="true" style="position: absolute; right: 8px; top: 118px; z-index: 1; width: 104px; height: 104px; transform: rotate(-6deg); filter: drop-shadow(0 3px 6px rgba(30,43,36,0.3))">'
 '<svg width="104" height="104" viewBox="0 0 104 104" style="display: block">'
 '<defs><path id="nbSealRim" d="M52 52 m-38 0 a38 38 0 1 1 76 0 a38 38 0 1 1 -76 0"/></defs>'
 '<circle cx="52" cy="52" r="51" fill="'+GREEN+'"/><circle cx="52" cy="52" r="47.5" fill="none" stroke="'+GOLD+'" stroke-width="1"/><circle cx="52" cy="52" r="28.5" fill="none" stroke="'+GOLD+'" stroke-width="1"/>'
 '<g style="transform-box: view-box; transform-origin: 52px 52px; animation: acSpin 36s linear infinite"><text fill="'+CREAM+'" style="font-family: Montserrat, sans-serif; font-size: 8.4px; font-weight: 600; letter-spacing: 0.16em"><textPath href="#nbSealRim" textLength="232" lengthAdjust="spacing">BUFFET NAVIDEÑO ✦ DJS ✦ VINO POR MESA ✦</textPath></text></g>'
 '<path d="'+STAR+'" fill="'+GOLD+'"/></svg></div>')
LI=lambda col,shape,txt:'<li style="display: flex; align-items: baseline; gap: 10px"><svg aria-hidden="true" width="12" height="12" viewBox="0 0 12 12" fill="%s" style="flex-shrink: 0; position: relative; top: 1px">%s</svg><span>%s</span></li>'%(col,shape,txt)
PRICE=lambda a,b:('<div style="display: flex; align-items: baseline; gap: 8px"><span style="font-family: \'Cormorant Garamond\', serif; font-size: 20px">%s</span><span aria-hidden="true" style="flex-grow: 1; border-bottom: 1px dotted '+GREEN+'"></span><span style="font-weight: 600; letter-spacing: 0.02em; font-family: var(--font-display); font-size: 14px; color: '+RED+'">%s</span></div>')%(a,b)
CAL=('https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=Cena+de+Nochebuena+en+AC+Hotel+Punta+Cana&amp;dates=20261224T223000Z/20261225T023000Z'
     '&amp;location=AC+Hotel+Punta+Cana,+Av.+Barcel%C3%B3+Km+9,+B%C3%A1varo&amp;details=Buffet+navide%C3%B1o,+DJs+y+vino+por+mesa.+Reserva+por+WhatsApp.')
BTN='display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; text-decoration: none'
SLEIGH=('<div aria-hidden="true" style="position: relative; height: 46px; margin: 20px -18px -18px; overflow: visible; container-type: inline-size; z-index: 2; border-bottom: 1px dotted '+GREEN+'; pointer-events: none">'
 '<span style="position: absolute; left: 0; bottom: 2px; transform-origin: 30% 100%; animation: acSantaFly 15s linear infinite"><svg width="136" height="40" viewBox="0 0 136 40" style="display: block; overflow: visible; animation: acHop 0.7s ease-in-out infinite alternate">'
 # saco y Santa
 '<circle cx="14" cy="20" r="7" fill="#7A5236"/><path d="M11 13 q3 -3 6 0" stroke="'+GOLD+'" stroke-width="1.2" fill="none"/>'
 '<path d="M20 26 v-8 q0 -6 6 -6 q6 0 6 6 v8z" fill="'+RED+'"/><path d="M20 22 h12" stroke="'+CREAM+'" stroke-width="2"/>'
 '<circle cx="26" cy="9" r="3.6" fill="#F2C9A0"/><circle cx="24.7" cy="8.8" r="0.45" fill="#3A2418"/><circle cx="27.3" cy="8.8" r="0.45" fill="#3A2418"/><path d="M22.4 10.4 q3.6 6.2 7.2 0 z" fill="#FFFFFF"/>'
 '<path d="M22.6 5.2 C23 1 25.5 -2.2 29 -2.4 C31.6 -2.5 33.2 -0.6 33.6 2.4 L31.8 2.6 C31.4 1.2 30.6 0.4 29.6 0.6 C29.9 2.2 30 4 29.8 5.2 Z" fill="'+RED+'"/>'
 '<rect x="21.6" y="4.2" width="8.8" height="2.4" rx="1.3" fill="#FFFFFF"/><circle cx="33" cy="3.4" r="1.7" fill="#FFFFFF"/>'
 # trineo
 '<path d="M8 24 h34 l-3 8 h-27 q-5 0 -4 -8z" fill="'+RED+'"/><path d="M12 28 h26" stroke="'+GOLD+'" stroke-width="1"/>'
 '<path d="M6 36 q1 2 6 2 h30 q5 0 6 -5" stroke="'+GOLD+'" stroke-width="1.6" fill="none" stroke-linecap="round"/><path d="M15 32 v4 M36 32 v4" stroke="'+GOLD+'" stroke-width="1.4"/>'
 # riendas
 '<path d="M40 25 q20 -2 40 -6 q14 -2 30 -4" stroke="'+GOLD+'" stroke-width="0.8" fill="none"/>'
 # renos
 + ''.join('<g transform="translate(%d %d)"><ellipse cx="0" cy="0" rx="8" ry="4" fill="#7A5236"/><path d="M-5 3 l-2 8 M-2 4 l0 8 M3 4 l1 8 M6 3 l3 7" stroke="#7A5236" stroke-width="1.6" stroke-linecap="round"/><path d="M6 -2 l4 -6" stroke="#7A5236" stroke-width="2.4" stroke-linecap="round"/><circle cx="11" cy="-9" r="2.6" fill="#7A5236"/><path d="M10 -11 l-2 -5 M10 -11 l2 -5 M9 -14 l-3 -1 M11 -14 l3 -1" stroke="#7A5236" stroke-width="0.9" stroke-linecap="round"/><circle cx="13.4" cy="-8.4" r="%s" fill="%s"/></g>' % (x, y, r, c) for x, y, r, c in ((84, 22, '1', '#3A2418'), (112, 18, '1.6', RED)))
 + '</svg></span></div>\n')
card=('<sc-if value="{{showNoche}}" hint-placeholder-val="{{true}}">\n'
'<article data-fest-card="1" style="position: relative; margin-top: 36px; background: '+CREAM+'; border: 2px solid '+GREEN+'; color: '+INK+'; overflow: hidden; display: flex; flex-direction: column; animation: acRise 0.9s ease-out both">\n'+STRIP+'\n'
'<div style="position: relative; height: 176px; overflow: hidden; margin: 14px 14px 0; border: 1px solid '+GREEN+'"><img src="/_blob/b1aef0b756c24e6b2189b008c2b02ba7" alt="Árbol de Navidad dorado en el lobby del hotel" style="width: 100%; height: 100%; object-fit: cover; display: block; animation: acZoom 10s ease-out both"></div>\n'+SEAL+'\n'
'<div style="flex-grow: 1; padding: 18px 18px 18px; display: flex; flex-direction: column">\n'
'<div style="align-self: flex-start; background: '+RED+'; color: '+CREAM+'; padding: 7px 12px; font-family: var(--font-display); font-size: 10px; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase">Jue 24 dic · 6:30 pm · {{ cdNoche }}</div>\n'
'<h3 style="margin: 14px 0 0; display: flex; flex-direction: column; max-width: calc(100% - 84px)"><span style="font-family: \'Cormorant Garamond\', serif; font-weight: 500; font-size: 26px; line-height: 28px; color: '+INK+'">Cena de</span><span style="font-family: \'Cormorant Garamond\', serif; font-style: italic; font-weight: 600; font-size: 44px; line-height: 44px; color: '+RED+'">Nochebuena</span></h3>\n'
'<p style="margin: 10px 0 0; font-family: \'Cormorant Garamond\', serif; font-style: italic; font-size: 20px; line-height: 25px; color: '+INK+'">Para celebrar en familia la noche del 24.</p>\n'
'<ul style="margin: 16px 0 0; padding: 14px 0 0; border-top: 2px dotted '+GREEN+'; list-style: none; display: flex; flex-direction: column; gap: 5px; font-family: \'Cormorant Garamond\', serif; font-size: 19px; line-height: 24px; color: '+INK+'">'
+LI(GREEN,'<circle cx="6" cy="6" r="5"/>','Buffet navideño')+LI(RED,'<path d="M6 0l6 6-6 6-6-6z"/>','DJs')+LI(GOLD,'<path d="M6 0l1.8 3.9 4.2.5-3.1 2.9.8 4.2L6 9.4 2.3 11.5l.8-4.2L0 4.4l4.2-.5z"/>','Vino por mesa')+'</ul>\n'
'<div style="margin-top: 16px; padding: 12px 14px; background: #EEF0E4; display: flex; flex-direction: column; gap: 4px">'+PRICE('Adultos','US$75 + imp.')+PRICE('Niños','US$45 + imp.')+
'<div style="margin-top: 4px; font-size: 12px; line-height: 17px; color: #46524A">Precios + 28% de impuestos.</div></div>\n'
'<a href="https://wa.link/hwnaf7" target="_blank" rel="noopener noreferrer" style="margin-top: 18px; min-height: 52px; background: '+RED+'; color: '+CREAM+'; font-size: 12px; '+BTN+'">Escríbenos para asistir</a>\n'
'<a href="'+CAL+'" target="_blank" rel="noopener noreferrer" style="margin-top: 10px; min-height: 44px; border: 1px solid '+INK+'; color: '+INK+'; font-size: 11px; '+BTN+'">Guárdalo en tu calendario</a>\n'
+SLEIGH+'</div>\n'+STRIP.replace('"></div>','; transform: scaleY(-1)"></div>')+'\n</article>\n</sc-if>')
s=s[:i]+card+s[j:]
assert 'Thanksgiving' not in s, s.count('Thanksgiving')
s=s.replace('<title>Landing AC Hotel Punta Cana, celular, versión 2</title>','<title>Landing AC Hotel Punta Cana, celular, versión 2</title>',1)
s=s.replace('style="position: relative; margin-top: 18px; border: 1px solid var(--ac-near-black); background: var(--ac-near-black); padding: 0 16px 18px;','style="position: relative; margin-top: 34px; border: 1px solid var(--ac-near-black); background: var(--ac-near-black); padding: 0 16px 18px;')
s=s.replace('</style>','@keyframes acSantaFly{0%{transform:translate(-150px,0) rotate(0)}38%{transform:translate(calc(48cqw - 68px),0) rotate(0)}50%{transform:translate(calc(68cqw - 68px),-26px) rotate(-10deg)}68%{transform:translate(calc(100cqw + 30px),-240px) rotate(-16deg)}100%{transform:translate(calc(100cqw + 30px),-240px) rotate(-16deg)}}</style>',1)
open(S+'/canvas/project/V2-navidad.dc.html','w',encoding='utf-8').write(s); print('ok')

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
def runner(col, sc=1):
    return ('<g fill="none" stroke="'+col+'" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" transform="scale(%s)">'%sc+
      '<circle cx="15" cy="5" r="3.2" fill="'+col+'" stroke="none"/><path d="M14 9 L11 19"/><path d="M11 19 L16 25 L14 31"/><path d="M11 19 L7 25 L2 26"/>'
      '<path d="M13 12 L18 15 L21 12"/><path d="M13 12 L8 14 L6 18"/></g>')
PIN='<span style="position: absolute; width: 7px; height: 7px; border-radius: 50%; background: #C9C9D6; box-shadow: inset 0 1px 1px rgba(0,0,0,0.35); {p}"></span>'
BIB=('<div aria-hidden="true" style="position: relative; align-self: center; margin-top: 20px; width: 236px; background: '+W+'; color: '+IND+'; padding: 12px 16px 12px; box-sizing: border-box; box-shadow: 0 10px 24px rgba(10,0,80,0.35); transform: rotate(-3deg); transform-origin: 50% 0; animation: acBib 4s ease-in-out infinite alternate; text-align: center">'
 +PIN.format(p='left: 8px; top: 8px')+PIN.format(p='right: 8px; top: 8px')+PIN.format(p='left: 8px; bottom: 8px')+PIN.format(p='right: 8px; bottom: 8px')+
 '<div style="background: '+MAG+'; color: '+W+'; margin: 6px 6px 0; padding: 4px 0; font-family: var(--font-display); font-size: 8px; font-weight: 600; letter-spacing: 0.12em; white-space: nowrap; text-transform: uppercase">San Silvestre del Caribe 2026</div>'
 '<div style="font-family: var(--font-display); font-weight: 700; font-size: 84px; line-height: 84px; letter-spacing: -0.04em; margin-top: 4px">27</div>'
 '<div style="font-family: var(--font-display); font-weight: 600; font-size: 12px; letter-spacing: 0.26em; text-transform: uppercase">Dic · 5K · 10K</div></div>')
RUN=('<div aria-hidden="true" style="position: relative; height: 40px; margin-top: 22px; container-type: inline-size; overflow: hidden; border-bottom: 1px dashed rgba(255,255,255,0.35); pointer-events: none">'
 '<span style="position: absolute; left: 0; bottom: 3px; animation: acRun 6s linear infinite"><svg width="26" height="32" viewBox="0 0 26 32" style="display: block; overflow: visible; animation: acHop 0.35s ease-in-out infinite alternate">'+runner(W)+'</svg></span>'
 '<span style="position: absolute; left: 0; bottom: 3px; animation: acRun 6s -2.4s linear infinite"><svg width="26" height="32" viewBox="0 0 26 32" style="display: block; overflow: visible; animation: acHop 0.38s ease-in-out infinite alternate">'+runner(PINK)+'</svg></span></div>')
KIT=('<div style="margin-top: 18px; display: flex; gap: 12px; align-items: flex-start; padding: 14px; border: 1px solid rgba(255,255,255,0.35)">'
 '<svg aria-hidden="true" width="26" height="26" viewBox="0 0 26 26" fill="none" stroke="'+PINK+'" stroke-width="1.6" stroke-linejoin="round" style="flex-shrink: 0"><path d="M4 9h18l-1.5 14h-15z"/><path d="M9 9V6.5a4 4 0 0 1 8 0V9"/></svg>'
 '<div style="display: flex; flex-direction: column; gap: 3px"><span style="font-family: var(--font-display); font-weight: 600; font-size: 15px; line-height: 20px">Recoge tu kit en AC Hotel</span>'
 '<span style="font-size: 13px; line-height: 19px; color: rgba(255,255,255,0.85)">[por confirmar: días y horario de entrega de kits]</span></div></div>')
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
KF="@keyframes acRun{from{transform:translateX(-40px)}to{transform:translateX(calc(100cqw + 20px))}}@keyframes acBib{from{transform:rotate(-3deg)}to{transform:rotate(-1deg)}}"
s=s.replace('</style>',KF+'</style>',1)
assert 'Nochebuena' not in re.sub(r'<script.*?</script>','',s,flags=re.S).replace('cdNoche',''), 'quedó Nochebuena'
open(S+'/canvas/project/V2-carrera.dc.html','w',encoding='utf-8').write(s); print('ok')

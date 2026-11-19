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
def runner(col, dur=0.62):
    T=dur; H=T/2
    def limb(origin, kf, delay, body):
        return ('<g style="transform-box: view-box; transform-origin: %s; animation: %s %.2fs %.2fs linear infinite">%s</g>'%(origin,kf,T,delay,body))
    def leg(c, d):
        return limb('19px 30px','acThigh',d,'<path d="M15.6 30 C16 27.5 22 27.5 22.4 30 L20.9 42 C20.4 43.6 17.6 43.6 17.1 42 Z" fill="'+c+'"/>'
               +limb('19px 42px','acShin',d,'<path d="M16.9 42 C17.5 40.6 20.5 40.6 21.1 42 L20.3 51.5 C20 52.6 18 52.6 17.7 51.5 Z" fill="'+c+'"/><path d="M17.4 51 C17.6 50 20.6 50.2 21.2 50.8 L25.4 52.2 C26.4 52.7 26 54.3 25 54.3 L18.2 54.3 C17.2 54.3 16.9 52.4 17.4 51 Z" fill="'+c+'"/>'))
    def arm(c, d):
        return limb('23.6px 16px','acUpper',d,'<path d="M21.7 16 C22 14.4 25.2 14.4 25.5 16 L24.8 24.6 C24.5 25.8 22.7 25.8 22.4 24.6 Z" fill="'+c+'"/>'
               +limb('23.6px 24.6px','acFore',d,'<path d="M22.3 24.6 C22.6 23.4 24.6 23.4 24.9 24.6 L24.3 31.4 C24.2 32.6 23 32.6 22.9 31.4 Z" fill="'+c+'"/><circle cx="23.6" cy="32.2" r="1.5" fill="'+c+'"/>'))
    far='rgba(255,255,255,0.42)' if col=='#FFFFFF' else 'rgba(255,155,214,0.45)'
    torso=('<path d="M21.2 12.8 C24.6 11.4 28.4 12.6 27.8 16 L23.8 30.6 C22.8 33 16.4 33 16.2 30 Z" fill="'+col+'"/>'
           '<path d="M24.8 10.4 L26 13.6" stroke="'+col+'" stroke-width="3" stroke-linecap="round"/><circle cx="27.4" cy="7.4" r="4.3" fill="'+col+'"/>')
    return '<g transform="rotate(7 19 30)">'+arm(far,-H)+leg(far,-H)+torso+leg(col,0)+arm(col,0)+'</g>'
PIN='<span style="position: absolute; width: 7px; height: 7px; border-radius: 50%; background: #C9C9D6; box-shadow: inset 0 1px 1px rgba(0,0,0,0.35); {p}"></span>'
BIB=('<div aria-hidden="true" style="position: relative; align-self: center; margin-top: 20px; width: 236px; background: '+W+'; color: '+IND+'; padding: 12px 16px 12px; box-sizing: border-box; box-shadow: 0 10px 24px rgba(10,0,80,0.35); transform: rotate(-3deg); transform-origin: 50% 0; animation: acBib 4s ease-in-out infinite alternate; text-align: center">'
 +PIN.format(p='left: 8px; top: 8px')+PIN.format(p='right: 8px; top: 8px')+PIN.format(p='left: 8px; bottom: 8px')+PIN.format(p='right: 8px; bottom: 8px')+
 '<div style="background: '+MAG+'; color: '+W+'; margin: 6px 6px 0; padding: 4px 0; font-family: var(--font-display); font-size: 8px; font-weight: 600; letter-spacing: 0.12em; white-space: nowrap; text-transform: uppercase">San Silvestre del Caribe 2026</div>'
 '<div style="font-family: var(--font-display); font-weight: 700; font-size: 84px; line-height: 84px; letter-spacing: -0.04em; margin-top: 4px">27</div>'
 '<div style="font-family: var(--font-display); font-weight: 600; font-size: 12px; letter-spacing: 0.26em; text-transform: uppercase">Dic · 5K · 10K</div></div>')
RUN=('<div aria-hidden="true" style="position: relative; height: 66px; margin-top: 18px; container-type: inline-size; overflow: hidden; border-bottom: 1px dashed rgba(255,255,255,0.35); pointer-events: none">'
 '<span style="position: absolute; left: 0; bottom: 1px; animation: acRun 7s linear infinite"><svg width="40" height="58" viewBox="0 0 40 58" style="display: block; overflow: visible; animation: acBob 0.31s ease-in-out infinite alternate">'+runner(W)+'</svg></span>'
 '<span style="position: absolute; left: 0; bottom: 1px; animation: acRun 7.6s -3.1s linear infinite"><svg width="36" height="52" viewBox="0 0 40 58" style="display: block; overflow: visible; animation: acBob 0.33s ease-in-out infinite alternate">'+runner(PINK,0.66)+'</svg></span></div>')
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
KF="@keyframes acRun{from{transform:translateX(-50px)}to{transform:translateX(calc(100cqw + 20px))}}@keyframes acBob{from{transform:translateY(0)}to{transform:translateY(-3px)}}@keyframes acThigh{0%{transform:rotate(-42deg)}50%{transform:rotate(32deg)}100%{transform:rotate(-42deg)}}@keyframes acShin{0%{transform:rotate(18deg)}20%{transform:rotate(8deg)}50%{transform:rotate(55deg)}70%{transform:rotate(105deg)}100%{transform:rotate(18deg)}}@keyframes acUpper{0%{transform:rotate(48deg)}50%{transform:rotate(-55deg)}100%{transform:rotate(48deg)}}@keyframes acFore{0%{transform:rotate(-70deg)}50%{transform:rotate(-110deg)}100%{transform:rotate(-70deg)}}@keyframes acBib{from{transform:rotate(-3deg)}to{transform:rotate(-1deg)}}"
s=s.replace('</style>',KF+'</style>',1)
assert 'Nochebuena' not in re.sub(r'<script.*?</script>','',s,flags=re.S).replace('cdNoche',''), 'quedó Nochebuena'
open(S+'/canvas/project/V2-carrera.dc.html','w',encoding='utf-8').write(s); print('ok')

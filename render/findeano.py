import re, os
S = os.environ.get('KIT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=open(S+'/canvas/project/V2-carrera.dc.html',encoding='utf-8').read()
BLK,GOLD,CHAMP,CRM='#161514','#C9A24A','#E9D8A6','#F6EFE2'
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
STAR4='M0 -6 C0.8 -1.4 1.4 -0.8 6 0 C1.4 0.8 0.8 1.4 0 6 C-0.8 1.4 -1.4 0.8 -6 0 C-1.4 -0.8 -0.8 -1.4 0 -6Z'
def stars(w=300,n=11):
    out=['<svg aria-hidden="true" width="%d" height="40" viewBox="0 0 %d 40" style="position: absolute; left: 50%%; top: 0; transform: translateX(-50%%); overflow: visible; pointer-events: none">'%(w,w)]
    for i in range(n):
        x=14+i*(w-28)/(n-1); L=[10,18,13,22,15][i%5]; sc=[0.9,1.3,1.0,1.5,1.1][i%5]; c=[GOLD,CHAMP][i%2]
        out.append('<g style="transform-box: fill-box; transform-origin: 50%% 0; animation: acFlag %.1fs %.2fs ease-in-out infinite alternate"><g transform="translate(%.1f 0)"><path d="M0 0 V%d" stroke="%s" stroke-width="0.7" opacity="0.8"/><g transform="translate(0 %.1f)"><path d="%s" fill="%s" transform="scale(%s)" style="transform-box: fill-box; transform-origin: center; animation: acTwinkle %.1fs %.1fs ease-in-out infinite"/></g></g></g>'%((2.4,2.8,3.2)[i%3],(i%5)*0.3,x,L,GOLD,L+6*sc,STAR4,c,sc,(2.4,3.0,2.7)[i%3],(i%4)*0.6))
    out.append('</svg>'); return ''.join(out)
DECO='repeating-linear-gradient(135deg, '+GOLD+' 0 4px, '+BLK+' 4px 9px)'
i=s.index('<sc-if value="{{agenda.fest}}"'); j=s.index('</sc-if>',i)+8
s=s[:i]+'<sc-if value="{{agenda.fest}}" hint-placeholder-val="{{true}}">'+stars()+'</sc-if>'+s[j:]
i=s.index('<sc-if value="{{agenda.fest}}"',i+40); j=s.index('</sc-if>',i)+8
s=s[:i]+'<sc-if value="{{agenda.fest}}" hint-placeholder-val="{{true}}"><span aria-hidden="true" style="position: absolute; left: 0; right: 0; bottom: 0; height: 10px; background: '+DECO+'"></span></sc-if>'+s[j:]
rep(" { y: 2026, m: 12, d: 27, name: 'San Silvestre del Caribe', href: '#comunidad' },\n","")
k=s.index('var isFest'); e=s.index('\n',s.index('var agenda',k)); line=s[k:e]
for a,b in [("nx.name === 'San Silvestre del Caribe'","nx.name === 'Gran Cena de Fin de Año'"),("name1: isFest ? 'San Silvestre ' : nx.name","name1: isFest ? 'Gran Cena de ' : nx.name"),
            ("name2: isFest ? 'del Caribe' : ''","name2: isFest ? 'Fin de Año' : ''"),("bg: isFest ? '#14009A'","bg: isFest ? '"+BLK+"'"),("ink: isFest ? '#FFFFFF'","ink: isFest ? '"+CRM+"'"),
            ("eyebrow: isFest ? '#FF9BD6'","eyebrow: isFest ? '"+GOLD+"'"),("accent: isFest ? '#FF9BD6'","accent: isFest ? '"+CHAMP+"'"),("border: isFest ? '0'","border: isFest ? '1px solid "+GOLD+"'")]:
    assert line.count(a)>=1,(a,line); line=line.replace(a,b)
s=s[:k]+line+s[e:]
# sale la carrera
i=s.index('<sc-if value="{{showSS}}"'); j=s.index('</sc-if>',s.index('</section>',i))+8; s=s[:i]+s[j:].lstrip('\n')
assert 'San Silvestre' not in re.sub(r'<script.*?</script>','',s,flags=re.S), 'quedó la carrera'
open(S+'/canvas/project/V2-findeano.dc.html','w',encoding='utf-8').write(s); print('ok')

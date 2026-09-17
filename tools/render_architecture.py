"""Render the illustrative profile animation. Requires Pillow; no network calls."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(parents=True, exist_ok=True)
W, H, SCALE = 1200, 650, 2
BG = '#0b1224'
INK = '#edf4fc'
MUTED = '#adc0d7'
CYAN = '#5eead4'
BLUE = '#71baff'
RED = '#ff6b8b'
GREEN = '#6ee7b7'

def font(size, bold=False):
    candidates = [Path('C:/Windows/Fonts') / ('segoeuib.ttf' if bold else 'segoeui.ttf'),
                  Path('/usr/share/fonts/truetype/dejavu') / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    return ImageFont.truetype(str(next(p for p in candidates if p.exists())), round(size*SCALE))

FONTS = {(s,b): font(s,b) for s in (16,18,20,22,24,26,28,30,48) for b in (False,True)}

def draw_frame(t):
    im = Image.new('RGB', (W*SCALE, H*SCALE), BG)
    d = ImageDraw.Draw(im)
    def rr(box, fill, outline=None, r=14, width=1):
        d.rounded_rectangle(tuple(round(a*SCALE) for a in box), radius=round(r*SCALE),
                            fill=fill, outline=outline, width=round(width*SCALE))
    def line(points, fill, width=2):
        d.line([(round(x*SCALE),round(y*SCALE)) for x,y in points], fill=fill, width=round(width*SCALE), joint='curve')
    def txt(x,y,text,size=20,color=INK,bold=False,anchor=None):
        d.text((round(x*SCALE),round(y*SCALE)),text,font=FONTS[(size,bold)],fill=color,anchor=anchor)
    def circle(x,y,r,fill,outline=None,width=1):
        d.ellipse(tuple(round(a*SCALE) for a in (x-r,y-r,x+r,y+r)),fill=fill,outline=outline,width=round(width*SCALE))
    def check(x,y,color=GREEN):
        line([(x,y+5),(x+5,y+10),(x+16,y-3)],color,2)
    def pulse(x,y,color):
        circle(x,y,15,'#173e4c')
        circle(x,y,9,color)
        circle(x,y,3,'#ffffff')
    def arrow(x,y,color,right=True):
        sign=1 if right else -1
        line([(x-sign*7,y-6),(x,y),(x-sign*7,y+6)],color,2)

    # Restrained grid and accent: motion only belongs to the request.
    for x in range(30,W,40):
        for y in range(25,H,40): circle(x,y,0.75,'#1c2a40')
    rr((2,2,W-2,H-2),None,'#243951',20)
    rr((46,40,52,173),CYAN,r=3)
    txt(72,37,'ENGENHEIRO DE SOFTWARE  /  FULL STACK',18,CYAN,True)
    txt(69,67,'Márcio Lima',48,INK,True)
    txt(72,133,'APIs, sistemas corporativos, web e mobile.',24,MUTED)
    txt(1152,45,'@TzMarcio',20,MUTED,anchor='ra')
    rr((936,87,1153,125),'#142c3b','#2c5963',19)
    circle(957,106,4,CYAN)
    txt(973,94,'6+ anos de experiência',16,INK)
    line([(46,194),(1154,194)],'#263851',1)
    txt(46,211,'DA INTERFACE À INTEGRAÇÃO',18,CYAN,True)
    txt(1154,211,'Um fluxo, três camadas.',18,MUTED,anchor='ra')

    # All three labels remain readable throughout every phase.
    phase = 0 if t < 1.5 else 1 if t < 4.9 else 2 if t < 6.6 else 3
    active = 0 if phase in (0,3) else phase
    cards=[(46,264,346,485),(450,264,750,485),(854,264,1154,485)]
    colors=[RED,BLUE,CYAN]
    for i,(x,y,x2,y2) in enumerate(cards):
        rr((x,y,x2,y2),'#111e32',colors[i] if i==active else '#2b3f59',16,2 if i==active else 1)
        txt(x+20,y+15,['01 / INTERFACE','02 / BACKEND','03 / INTEGRAÇÃO'][i],16,colors[i],True)
    # Angular-inspired shield with a clear typographic mark.
    d.polygon([(round(x*SCALE),round(y*SCALE)) for x,y in [(66,318),(83,312),(100,318),(97,338),(83,347),(69,338)]],fill=RED)
    txt(83,312,'A',24,BG,True,anchor='ma')
    txt(112,314,'Angular',28,INK,True)
    txt(67,353,'TypeScript · Experiência web',18,MUTED)
    rr((66,391,326,423),'#0b1629','#263d55',7)
    txt(79,396,'Nova solicitação',18,MUTED)
    success=t>=8.0
    rr((66,439,326,469),GREEN if success else '#953550',r=7)
    txt(196,439,'Concluído' if success else 'Enviar solicitação',18,BG if success else INK,True,anchor='ma')
    if success: check(81,445,BG)

    # API mark, instead of terminal imagery.
    rr((470,315,504,350),'#182e49','#417198',7)
    txt(487,316,'{ }',22,BLUE,True,anchor='ma')
    txt(516,314,'Java / Quarkus',26,INK,True)
    txt(470,353,'API REST · Regra de negócio',18,MUTED)
    for i,(label,threshold) in enumerate([('Contrato REST',2.3),('Validação',3.1),('Regra de negócio',3.9)]):
        y=393+i*25
        if t>=threshold: check(473,y+2)
        else: circle(480,y+9,5,'#263e58')
        txt(503,y,label,18,INK if t>=threshold else MUTED)

    rr((874,315,908,350),'#123a3e','#2c7774',7)
    for x,y in [(883,324),(899,324),(891,340)]:
        rr((x-3,y-3,x+3,y+3),CYAN,r=1)
    line([(883,324),(899,324),(891,340),(883,324)],CYAN,1)
    txt(920,314,'Sistemas',28,INK,True)
    txt(874,353,'ERPs · Serviços externos',18,MUTED)
    rr((874,397,981,437),'#162c40','#35516a',8)
    rr((1027,397,1134,437),'#162c40','#35516a',8)
    txt(928,403,'ERP',20,INK,True,anchor='ma')
    txt(1080,403,'Serviços',20,INK,True,anchor='ma')
    line([(981,417),(1027,417)],CYAN if t>=5.4 else '#3b6073',2)
    arrow(1022,417,CYAN if t>=5.4 else '#3b6073')
    if t>=6.0:
        check(876,453)
        txt(900,445,'Integração concluída',18,GREEN)
    else: txt(875,445,'Contratos entre sistemas',18,MUTED)

    # Request travels horizontally; the response has a separate return route.
    line([(348,368),(448,368)],'#365369',2)
    line([(752,368),(852,368)],'#365369',2)
    arrow(438,368,BLUE)
    arrow(842,368,CYAN)
    txt(397,334,'REST',16,MUTED,True,anchor='ma')
    txt(803,334,'API',16,MUTED,True,anchor='ma')
    line([(1004,487),(1004,553),(196,553),(196,487)],'#345261',2)
    arrow(589,553,'#568992',False)
    rr((455,505,745,543),BG,r=15)
    txt(600,508,'Resposta para a interface',18,MUTED,anchor='ma')
    def ease(v): return v*v*(3-2*v)
    if 1.5<=t<2.3: pulse(348+100*ease((t-1.5)/.8),368,BLUE)
    if 4.1<=t<4.9: pulse(752+100*ease((t-4.1)/.8),368,CYAN)
    if 6.6<=t<8.0:
        v=(t-6.6)/1.4
        if v<.15: pulse(1004,487+66*ease(v/.15),GREEN)
        elif v<.85:
            x=1004-808*ease((v-.15)/.70)
            pulse(x,553,GREEN)
        else: pulse(196,553-66*ease((v-.85)/.15),GREEN)

    rr((46,586,1154,626),'#102136','#294257',11)
    labels=['01  /  A interface inicia a solicitação',
            '02  /  A API valida o contrato e aplica a regra de negócio',
            '03  /  A integração conecta aplicações e serviços',
            '04  /  A resposta volta para a experiência do usuário']
    circle(67,606,4,[RED,BLUE,CYAN,GREEN][phase])
    txt(82,592,labels[phase],20,INK)
    txt(1154,560,'Arquitetura ilustrativa',16,MUTED,anchor='ra')
    return im.resize((W,H),Image.Resampling.LANCZOS)

frames=[draw_frame(i*.08) for i in range(125)]
# One palette across frames avoids color shimmer and reduces file size.
palette=draw_frame(8.5).quantize(colors=192,method=Image.Quantize.MEDIANCUT)
frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
frames[0].save(OUT/'architecture-flow.gif',save_all=True,append_images=frames[1:],
               duration=80,loop=0,optimize=True,disposal=1)
draw_frame(8.5).save(OUT/'architecture-flow-static.png',optimize=True)
# Contact sheet for visual inspection, not published.
sheet=Image.new('RGB',(W,3*H))
for i,t in enumerate((.8,3.5,8.5)): sheet.paste(draw_frame(t),(0,i*H))
review=ROOT.parents[1]/'work'/'github-profile'
review.mkdir(parents=True,exist_ok=True)
sheet.save(review/'architecture-review.png')
print(f'GIF: {(OUT/"architecture-flow.gif").stat().st_size:,} bytes; 125 frames; 10 s')

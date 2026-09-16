"""Generate the VEXA PDF handoff from the supplied screen exports.
Uses Pillow and ReportLab. Run from any directory after tools/export_screens.py.
"""
from pathlib import Path
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from xml.sax.saxutils import escape
import json

ROOT=Path(__file__).resolve().parents[1]
W,H=A4; M=44; CW=W-2*M
INK=HexColor('#171715');PAPER=HexColor('#f4f2ed');MUTED=HexColor('#66655e');LINE=HexColor('#cfcbc2');ACC=HexColor('#b63823');SURF=HexColor('#e9e6df')
C=canvas.Canvas(str(ROOT/'VEXA-UIUX-Handoff.pdf'),pagesize=A4,pageCompression=1)
C.setTitle('VEXA / UI & UX Design Handoff');C.setAuthor('VEXA Concept Design');C.setSubject('Interactive prototype, visual system, editable-source handoff and verification scope')
page_no=0

def text(s,x,y,size=10,font='Helvetica',colour=INK):
    C.setFillColor(colour);C.setFont(font,size);C.drawString(x,H-y-size*.78,s)

def para(s,x,y,w=CW,size=10,colour=MUTED,leading=None):
    st=ParagraphStyle('body',fontName='Helvetica',fontSize=size,leading=leading or size*1.55,textColor=colour,spaceAfter=0)
    p=Paragraph(s,st);pw,ph=p.wrap(w,H);p.drawOn(C,x,H-y-ph);return y+ph

def line(y,x=M,w=CW):
    C.setStrokeColor(LINE);C.setLineWidth(.55);C.line(x,H-y,x+w,H-y)

def start(section,title,sub=None):
    global page_no
    page_no+=1;C.setFillColor(PAPER);C.rect(0,0,W,H,fill=1,stroke=0)
    C.bookmarkPage('p'+str(page_no));C.addOutlineEntry(section+' / '+title,'p'+str(page_no),0,False)
    text('VEXA',M,25,17,'Helvetica-Bold');text('DESIGN HANDOFF / 01',W-181,30,8,'Courier',MUTED);line(57)
    text(section.upper(),M,81,8,'Courier',ACC)
    text(title,M,104,33,'Helvetica-Bold')
    y=152
    if sub:y=para(sub,M,y,CW,10)+20
    C.setFillColor(MUTED);C.setFont('Courier',7);C.drawString(M,24,'VEXA CONCEPT / 16 SEP 2026');C.drawRightString(W-M,24,f'{page_no:02d} / 09')
    return y

def end():C.showPage()

def label(s,y,x=M,w=CW):
    text(s.upper(),x,y,8,'Courier',MUTED)

def image(name,x,y,w,h,top_crop=None):
    im=Image.open(ROOT/'preview'/f'{name}.png').convert('RGB')
    if top_crop:im=im.crop((0,0,im.width,min(top_crop,im.height)))
    ratio=min(w/im.width,h/im.height);dw=im.width*ratio;dh=im.height*ratio
    b=BytesIO();im.save(b,format='JPEG',quality=88,optimize=True);b.seek(0)
    C.setFillColor(SURF);C.rect(x,H-y-h,w,h,stroke=0,fill=1)
    C.drawImage(ImageReader(b),x+(w-dw)/2,H-y-dh,width=dw,height=dh)
    C.setStrokeColor(LINE);C.setLineWidth(.5);C.rect(x,H-y-h,w,h,stroke=1,fill=0)
    return y+h

def row(title,body,y,num=None):
    if num:text(num,M,y+1,8,'Courier',ACC)
    x=M+31 if num else M
    text(title,x,y,12,'Helvetica-Bold');ny=para(body,x,y+22,CW-(x-M),9.5);return ny+20

def table(rows,y,widths=None):
    widths=widths or [158,CW-158]
    for i,vals in enumerate(rows):
        styles=[];heights=[]
        for j,val in enumerate(vals):
            st=ParagraphStyle('cell',fontName='Helvetica-Bold' if i==0 else 'Helvetica',fontSize=8.5,leading=12,textColor=INK if j==0 else MUTED)
            p=Paragraph(val,st);pw,ph=p.wrap(widths[j]-18,H);styles.append((p,ph));heights.append(ph)
        rh=max(heights)+18
        if i==0:C.setFillColor(SURF);C.rect(M,H-y-rh,CW,rh,fill=1,stroke=0)
        x=M
        for j,(p,ph) in enumerate(styles):p.drawOn(C,x+9,H-y-9-ph);x+=widths[j]
        line(y+rh);y+=rh
    return y

# 01 / Cover
page_no=1;C.setFillColor(PAPER);C.rect(0,0,W,H,fill=1,stroke=0);C.bookmarkPage('p1');C.addOutlineEntry('01 / The store experience','p1')
text('VEXA',M,36,64,'Helvetica-Bold');text('DIGITAL COMMERCE / CONCEPT 01',M,117,9,'Courier',MUTED)
text('The store',M,153,41,'Helvetica-Bold');text('experience.',M,195,41,'Helvetica-Bold')
para('Interactive prototype. Editable source. A connected shopping journey.',M,256,CW,11)
image('01-home-desktop',M,304,CW,303,top_crop=850)
text('A DESIGN YOU CAN EXPLORE, NOT JUST LOOK AT.',M,629,8,'Courier',ACC)
para('Desktop and mobile layouts, working interface states and a documented design system for a premium streetwear concept.',M,650,CW,10)
line(703)
for i,(n,l) in enumerate([('22','EDITABLE SVG LAYOUTS'),('39','SCREEN EXPORTS'),('61','CHECKS PASSED')]):
    x=M+i*(CW/3);text(n,x,721,27,'Helvetica-Bold');text(l,x,756,7,'Courier',MUTED)
text('VEXA CONCEPT / 16 SEP 2026',M,809,7,'Courier',MUTED);C.setFont('Courier',7);C.drawRightString(W-M,27,'01 / 09');end()
# 02
Y=start('02 / Delivery','Start with the prototype.','The source is editable. The screens are individual. The interactions are connected. This package is a front-end design prototype, not a live commerce backend.')
Y=table([
 ['OPEN THIS','FOR THIS PURPOSE'],
 ['VEXA-Prototype.html','A portable, self-contained browser prototype. Code and concept images are embedded.'],
 ['preview/index.html','A gallery of all 39 desktop and mobile screen exports.'],
 ['design/screens/','22 SVG snapshots with editable text and shapes. Raster imagery remains raster.'],
 ['src/','The editable HTML-associated styles, catalogue data and interaction logic.'],
 ['design/tokens.json','Colours, type, spacing, controls and responsive reference values.'],
 ['docs/HANDOFF.md','The editable written specification and implementation notes.'],
 ['docs/qa-results.json','Results and limitations of the 61-check browser run.'],
],Y)
Y+=30;text('A complete demo journey.',M,Y,20,'Helvetica-Bold');Y=para('Home &gt; Collection &gt; Product &gt; Colour and size &gt; Bag &gt; Guest details &gt; Delivery &gt; Payment simulation &gt; Confirmation',M,Y+32,CW,11,INK)
Y+=25;Y=row('The quickest walkthrough','Open the prototype guide from the top bar. Load a sample bag, proceed to checkout and use sample details. Test a declined payment, then approve it. No real card, email delivery or order is involved.',Y)
para('<b>File format note:</b> the SVGs are editable layout snapshots, not native Figma Auto Layout frames, component variants or wired Figma prototypes. The HTML/CSS is the behavioural source of truth.',M,Y,CW,9)
end()
# 03
Y=start('03 / Visual system','Quiet interface. Strong identity.','Warm neutrals and a single action colour support editorial imagery without turning the shop into a decorative landing page.')
cols=[('PAPER','#F4F2ED'),('SURFACE','#E9E6DF'),('INK','#171715'),('MUTED','#66655E'),('ACCENT','#B63823'),('RULE','#CFCBC2')]
ww=(CW-50)/6
for i,(n,hx) in enumerate(cols):
    x=M+i*(ww+10);C.setFillColor(HexColor(hx));C.setStrokeColor(LINE);C.rect(x,H-Y-65,ww,65,fill=1,stroke=1);text(n,x,Y+77,7,'Courier',MUTED);text(hx,x,Y+91,7,'Courier',MUTED)
Y+=139;text('Built different.',M,Y,42,'Helvetica-Bold');Y+=66
Y=para('<b>Display:</b> Arial/Helvetica, 800-900 weight, tight tracking and fluid sizing. <b>Interface:</b> Arial/Helvetica, 12-16px. <b>Utility:</b> Courier New, small uppercase identifiers. System fallbacks keep the prototype self-contained; no font files are bundled.',M,Y,CW,10)
Y+=24;line(Y);Y+=24;text('Space creates the hierarchy.',M,Y,20,'Helvetica-Bold');Y+=35
Y=table([['LAYOUT RULE','REFERENCE'],['Desktop / mobile width','1440px / 390px'],['Outer margins','48px desktop, 30px intermediate, 20px mobile'],['Collection grid','Four columns on desktop; two on mobile'],['Control rhythm','52px primary buttons; 46px mobile purchase controls; 44px quantity and quick-option targets'],['Main breakpoints','360px, 760px, 1100px, 1600px'],['Motion','160ms controls / 240ms panels. Reduced-motion preference respected.']],Y)
para('Edit tokens in src/styles.css and keep design/tokens.json aligned. The JSON is documentation, not a live token compiler.',M,Y+22,CW,9)
end()
# 04
Y=start('04 / Discovery','From campaign to collection.','The homepage communicates the label first, then moves directly into garments. Browsing stays predictable even where editorial layouts are asymmetric.')
gap=16;col=(CW-gap)/2
image('01-home-desktop',M,Y,col,239,top_crop=1400);image('02-collection-desktop',M+col+gap,Y,col,239,top_crop=1400)
label('01 / Homepage',Y+252,M,col);label('02 / Collection',Y+252,M+col+gap,col)
Y+=292
Y=row('One clear first action','Shop the drop leads to new arrivals. The brand story and category links provide alternatives without adding competing promotional messages.',Y,'01')
Y=row('Useful filters, visible recovery','Category, size, colour, maximum price and sample availability combine with sorting. Active filters can be removed individually. No-results states lead back to the collection.',Y,'02')
Y=row('Cards lead to an informed choice','The plus control opens product options rather than adding an arbitrary size. Names, prices and colour information remain visible on touch devices.',Y,'03')
para('Review full-resolution screens in preview/. Crops on this page are overview illustrations, not the editable design files.',M,Y,CW,8.5)
end()
# 05
Y=start('05 / Product decisions','Make the garment the focus.','Large imagery, explicit options and accessible error recovery keep the purchase action clear.')
image('03-product-desktop',M,Y,CW,347,top_crop=985)
Y+=367
Y=row('Selection is never assumed','Colour selection updates the illustration. An available size is required before adding. A missing size produces an inline message and moves focus to the selector.',Y,'01')
Y=row('The same rules apply on mobile','The mobile purchase bar displays the price and selection state. It does not bypass size validation. Page-bottom spacing keeps content accessible behind the bar.',Y,'02')
para('<b>Asset limitation:</b> product photographs are low-resolution concept crops. Detail views are crops of the same image; chalk colourways are illustrative recolourings. Sample garment measurements are not real sizing advice.',M,Y,CW,9)
end()
# 06
Y=start('06 / Bag and checkout','A clear path to confirmation.','Guest checkout is split into details, delivery and review/payment. The order total is visible before the final simulation.')
image('06-checkout-details-desktop',M,Y,CW,342,top_crop=970)
Y+=362
Y=row('Totals stay connected','The sample bag contains a £160 hoodie and £180 cargo trousers: £340 subtotal. Standard sample delivery adds £12, producing a £352 demo total. Changing delivery updates the summary.',Y,'01')
Y=row('Errors preserve progress','Fields validate inline. A declined simulation leaves the bag and entered details intact. The success route produces a clearly labelled demo receipt and clears the demo bag.',Y,'02')
para('<b>No real payment form:</b> no card details are requested, no payment provider is connected and no confirmation email is sent. Contact details stay in page memory and disappear on refresh.',M,Y,CW,9)
end()
# 07
Y=start('07 / Mobile and states','Designed for the smaller screen.','Mobile navigation, drawers, purchase controls and form layouts are designed as responsive components, not scaled-down desktop pictures.')
gap=17;col=(CW-2*gap)/3
for i,(name,lbl,crop) in enumerate([('20-navigation-mobile','NAVIGATION',844),('17-filters-mobile','FILTERS',844),('08-checkout-payment-mobile','PAYMENT REVIEW',1000)]):
    x=M+i*(col+gap);image(name,x,Y,col,400,top_crop=crop);label(lbl,Y+412,x,col)
Y+=449
Y=row('States belong to the design','The export set includes empty bag, no search results, unavailable product, invalid input, adding/loading, selected options, declined payment and demo confirmation.',Y,'01')
Y=row('Keyboard and motion considered','Visible focus, labelled controls, modal containment, Escape-to-close and reduced-motion styling are implemented. These measures do not constitute a complete accessibility audit.',Y,'02')
end()
# 08
Y=start('08 / Source and verification','Built to inspect and modify.','The prototype uses plain HTML, CSS and JavaScript. No framework build process or external image/font request is required to view the portable file.')
Y=table([['SOURCE','RESPONSIBILITY'],['src/styles.css','Design tokens, reusable components and responsive rules.'],['src/catalogue.js','Eight sample products, illustrative GBP amounts, sizes, colours and stock fixtures.'],['src/app.js','Routes, search, filters, variant selection, bag state, validation and payment simulation.'],['build.py','Rebuild the portable HTML after editing the source.'],['serve.py','Optional local HTTP server. Run python3 serve.py.'],['tests/test_prototype.py','Repeatable browser checks, including recovery cases and fixture validation.']],Y)
Y+=30;text('61 checks passed.',M,Y,30,'Helvetica-Bold');Y=para('Chromium checks exercised the connected flow, size and email errors, filtering, quantities, totals, payment recovery, focus return, reduced motion and storage-sanitisation fixtures. No external network requests occurred in the run.',M,Y+46,CW,10)
Y+=25
Y=para('<b>Responsive scope:</b> homepage overflow checked at 320, 360, 390, 760, 768, 1100 and 1440px. Multiple additional routes checked at 390px. Desktop/mobile exports were reviewed visually.',M,Y,CW,9.5)
Y+=22
Y=para('<b>Environment:</b> headless Chromium using local HTML injection. Storage validation cases are mocked. Cross-session persistence, Safari, Firefox, screen readers and physical phones are not certified by this run.',M,Y,CW,9.5)
para('The exact results and exclusions are in docs/qa-results.json. A passing prototype check is not a production-security or accessibility certification.',M,Y+23,CW,9)
end()
# 09
Y=start('09 / Production review','The next layer is real commerce.','The design is explorable and editable. Real business content, services and validation still need to replace the demonstration fixtures.')
Y=row('Replace the concept material','Confirm the brand name, products, prices, stock, garment dimensions, photography and usage rights. VEXA is a working name. Existing artwork is generated concept imagery; upscaling does not create genuine product detail.',Y,'01')
Y=row('Connect the business systems','Add a real commerce catalogue, server-authoritative prices, destination-aware tax and shipping, payment gateway, order creation, transactional email and fulfilment. Add authenticated accounts only where needed.',Y,'02')
Y=row('Approve policies and support','Replace policy placeholders with business-approved privacy, terms, shipping and returns information. Supply real contact channels. No fake addresses, testimonials, guarantees or scarcity claims should replace missing information.',Y,'03')
Y=row('Validate with actual users','Test the prototype with intended shoppers. Check accessibility with assistive technology, real phones, enlarged text and keyboard use. Measure performance with approved production images under realistic network conditions.',Y,'04')
line(Y);Y+=22;text('Technical references',M,Y,14,'Helvetica-Bold');Y+=28
refs=[('MDN / Native modal behaviour','https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal'),('MDN / localStorage and local-file caveats','https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage'),('MDN / Reduced-motion preferences','https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion')]
for title,url in refs:
    text(title,M,Y,9,'Helvetica',MUTED);C.linkURL(url,(M,H-Y-12,W-M,H-Y+2),relative=0,thickness=0);Y+=23
para('Design assumptions are not user-research findings. No live orders, payments, subscriptions or customer data integrations are included in this handoff.',M,Y+11,CW,9)
end()
C.save()
print('Generated',ROOT/'VEXA-UIUX-Handoff.pdf')

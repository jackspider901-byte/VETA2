from pathlib import Path
from playwright.sync_api import sync_playwright
import json, shutil
P=Path(__file__).resolve().parents[1]
HTML=(P/'VEXA-Prototype.html').read_text(); SVG=(P/'tools/svg_export.js').read_text()
manifest=[]
with sync_playwright() as sp:
    exe=shutil.which('chromium') or shutil.which('google-chrome')
    browser=sp.chromium.launch(headless=True, **({'executable_path':exe} if exe else {}))
    for mode,w,h in [('desktop',1440,1000),('mobile',390,844)]:
        page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        page.set_content(HTML,wait_until='load')
        page.emulate_media(reduced_motion='reduce')
        def route(path):
            if page.locator('dialog').is_visible():page.keyboard.press('Escape')
            page.evaluate('(p)=>location.hash=p',path);page.wait_for_timeout(100)
        def save(name,label,svg=True,full=True):
            page.evaluate('scrollTo(0,0);document.querySelector("#toast").classList.remove("show")')
            page.wait_for_timeout(120)
            filename=f'{name}-{mode}'
            page.screenshot(path=str(P/'preview'/f'{filename}.png'),full_page=full,animations='disabled')
            if svg:
                out=page.evaluate(SVG);(P/'design/screens'/f'{filename}.svg').write_text(out)
            manifest.append({'file':filename,'title':label,'mode':mode,'width':w,'height':page.evaluate('document.documentElement.scrollHeight') if full else h,'svg':svg})
        save('01-home','Homepage')
        route('/shop');save('02-collection','Collection')
        route('/product/foundation-hoodie');page.get_by_role('button',name='Size M',exact=True).click();save('03-product','Product / size selected')
        page.get_by_role('button',name='Size guide',exact=False).first.click();save('18-size-guide','Size guide',False,False);page.keyboard.press('Escape')
        route('/bag');save('04-empty-bag','Empty bag',False)
        route('/guide');page.get_by_role('button',name='Load a sample bag').click();page.wait_for_timeout(100);save('05-bag','Shopping bag')
        page.get_by_role('button',name='Open shopping bag, 2 items',exact=True).click();save('19-bag-drawer','Shopping bag drawer',False,False);page.keyboard.press('Escape')
        route('/checkout');page.get_by_role('button',name='Use sample details').click();save('06-checkout-details','Checkout / details')
        page.get_by_role('button',name='Continue to delivery',exact=False).click();save('07-checkout-delivery','Checkout / delivery')
        page.get_by_role('button',name='Review & payment',exact=False).click();save('08-checkout-payment','Checkout / payment review')
        page.locator('input[name="payment"][value="declined"]').check();page.locator('#payment-button').click();page.wait_for_timeout(750);save('09-checkout-declined','Payment / declined state',False)
        page.locator('input[name="payment"][value="approved"]').check();page.locator('#payment-button').click();page.wait_for_timeout(750);save('10-confirmation','Demo confirmation')
        route('/about');save('11-about','Brand story')
        route('/lookbook');save('12-lookbook','Editorial lookbook')
        route('/design-system');save('13-design-system','Design system')
        route('/shop?q=zzzz');save('14-empty-results','No search results',False)
        route('/product/studio-cap');save('15-unavailable','Unavailable product',False)
        route('/shop');page.get_by_role('button',name='Search the collection',exact=True).click();page.locator('#search-input').fill('hoodie');save('16-search','Search suggestions',False,False);page.keyboard.press('Escape')
        page.get_by_role('button',name='Filters',exact=True).click();save('17-filters','Filter drawer',False,False);page.keyboard.press('Escape')
        if mode=='mobile':
            page.get_by_role('button',name='Open navigation').click();save('20-navigation','Mobile navigation',False,False);page.keyboard.press('Escape')
        page.close()
    browser.close()
(P/'design/screen-manifest.json').write_text(json.dumps(manifest,indent=2))
print('Exported',len(manifest),'screens and',sum(x['svg'] for x in manifest),'editable SVGs')

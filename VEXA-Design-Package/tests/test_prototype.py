"""Interaction checks using a local HTML injection, with no external network dependency.
Install development dependency: pip install playwright
Use an installed Chromium binary, or: playwright install chromium
Run from the package folder: python tests/test_prototype.py
Local file storage persistence is browser-dependent and is not certified by this harness.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, shutil, time
ROOT=Path(__file__).resolve().parents[1]
RESULTS=[]
def record(name,condition,detail=''):
    RESULTS.append({'check':name,'passed':bool(condition),'detail':detail})
    if not condition: raise AssertionError(name+': '+detail)

def run():
    html=(ROOT/'VEXA-Prototype.html').read_text()
    with sync_playwright() as sp:
        exe=shutil.which('chromium') or shutil.which('google-chrome')
        browser=sp.chromium.launch(headless=True,**({'executable_path':exe} if exe else {}),args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1440,'height':1000})
        page.set_default_timeout(6000)
        errors=[];requests=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda r:requests.append(r.url))
        page.set_content(html,wait_until='load')
        def route(path):
            page.evaluate('(p)=>{location.hash=p}',path);page.wait_for_timeout(90)
        record('Homepage renders',page.locator('h1').inner_text().replace('\n','')=='BUILTDIFFERENT.')
        record('Homepage loads every image',page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)'))
        for w in [1440,1100,768,760,390,360,320]:
            page.set_viewport_size({'width':w,'height':900});
            record(f'Homepage no horizontal overflow at {w}px',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.set_viewport_size({'width':1440,'height':1000})
        route('/shop');record('Catalogue has eight sample products',page.locator('.product-card').count()==8)
        page.locator('#sort').select_option('low');page.wait_for_timeout(100)
        record('Price sorting',page.locator('.product-card-info a').first.inner_text()=='Studio Cap')
        page.get_by_role('button',name='Filters',exact=True).click()
        page.locator('input[name="category"][value="Hoodies"]').check()
        page.get_by_role('button',name='Show results').click();page.wait_for_timeout(100)
        record('Category filter',page.locator('.product-card').count()==1)
        route('/shop?size=XL&available=1');names=page.locator('.product-card-info a').all_text_contents()
        record('Availability respects selected size','Foundation Hoodie' not in names and len(names)>0)
        route('/shop?q=zzzz-not-a-product');record('Empty search state',page.get_by_role('heading',name='Nothing here. Yet.').is_visible())
        page.get_by_role('link',name='Clear filters',exact=True).click();page.wait_for_timeout(100)
        record('Empty-state recovery',page.locator('.product-card').count()==8)
        page.get_by_role('button',name='Search the collection',exact=True).click()
        page.locator('#search-input').fill('hoodie');record('Search suggestions',page.locator('.suggestion-row').count()==1)
        page.keyboard.press('Escape');page.wait_for_timeout(80);record('Escape closes modal',not page.locator('dialog').is_visible())
        record('Focus restored after modal close',page.evaluate('document.activeElement.getAttribute("aria-label")')=='Search the collection')
        route('/product/foundation-hoodie')
        page.get_by_role('button',name='Add to bag',exact=True).first.click()
        record('Missing size blocked','Choose a size' in page.locator('#product-error').inner_text())
        record('Unavailable size disabled',page.get_by_role('button',name='Size XL, unavailable in demo',exact=True).is_disabled())
        page.get_by_role('button',name='Chalk',exact=True).click()
        record('Colour selector updates',page.get_by_role('button',name='Chalk',exact=True).get_attribute('aria-pressed')=='true')
        page.get_by_role('button',name='Size M',exact=True).click()
        page.get_by_role('button',name='Size guide',exact=False).first.click()
        page.get_by_role('button',name='Inches',exact=True).click()
        record('Size unit conversion','22.0' in page.locator('.size-table').inner_text())
        page.get_by_role('button',name='Close dialog').click()
        page.get_by_role('button',name='Detail crop',exact=True).click()
        record('Product gallery selection',page.locator('.gallery-main').get_attribute('data-view')=='1')
        page.get_by_role('button',name='Add to bag',exact=True).first.click()
        record('Add-to-bag loading state',page.locator('#add-button').get_attribute('aria-busy')=='true')
        page.wait_for_timeout(550)
        record('Bag drawer confirmation',page.locator('dialog').is_visible() and 'Added to your demo bag' in page.locator('dialog').inner_text())
        page.get_by_role('button',name='Increase Foundation Hoodie quantity',exact=True).click()
        record('Bag quantity updates',page.locator('.quantity-control span').inner_text()=='2')
        page.get_by_role('link',name='View bag',exact=True).click();page.wait_for_timeout(100)
        record('Full bag total updates','£320' in page.locator('.order-summary').inner_text())
        page.get_by_role('link',name='Continue to checkout',exact=False).click();page.wait_for_timeout(100)
        page.get_by_role('button',name='Continue to delivery',exact=False).click()
        record('Checkout validation','Enter an email address' in page.locator('#email-error').inner_text())
        page.get_by_role('button',name='Use sample details').click()
        page.get_by_role('button',name='Continue to delivery',exact=False).click()
        page.locator('input[name="shipping"][value="express"]').check()
        record('Delivery cost updates total','£342' in page.locator('.order-summary').inner_text())
        page.get_by_role('button',name='Review & payment',exact=False).click()
        record('Review retains contact details','jamie@example.com' in page.locator('.address-preview').inner_text())
        page.locator('input[name="payment"][value="declined"]').check()
        page.locator('#payment-button').click();page.wait_for_timeout(750)
        record('Declined payment recovery','unchanged' in page.locator('#payment-error').inner_text())
        record('Decline retains basket',page.locator('.summary-product').count()==1 and '£342' in page.locator('.order-summary').inner_text())
        page.locator('input[name="payment"][value="approved"]').check();page.locator('#payment-button').click();page.wait_for_timeout(750)
        record('Confirmation reached','/confirmation' in page.url and page.locator('.receipt').is_visible())
        record('Receipt total consistent','£342' in page.locator('.receipt').inner_text())
        record('No real-payment claim','No purchase was made' in page.locator('.confirmation-intro').inner_text())
        route('/bag');record('Bag cleared after demo order',page.get_by_role('heading',name='Room for something different.').is_visible())
        route('/product/studio-cap');record('Unavailable product state',page.get_by_role('button',name='Unavailable in this demo').is_disabled())
        page.get_by_role('button',name='Preview availability request').click();page.locator('#stock-email').fill('test@example.com');page.get_by_role('button',name='Preview request',exact=True).click()
        record('Availability request success','Nothing was sent or saved' in page.locator('#toast').inner_text())
        route('/');page.locator('#newsletter-email').fill('bad');page.locator('#newsletter-form button').click()
        record('Newsletter invalid state','valid email' in page.locator('#newsletter-note').inner_text())
        page.locator('#newsletter-email').fill('test@example.com');page.locator('#newsletter-form button').click()
        record('Newsletter demo success','Nothing was sent or saved' in page.locator('#newsletter-note').inner_text())
        page.set_viewport_size({'width':390,'height':844})
        page.get_by_role('button',name='Open navigation').click();record('Mobile navigation',page.locator('.menu-links').is_visible())
        page.locator('#overlay').get_by_role('link',name='Shop all',exact=True).click();page.wait_for_timeout(100)
        record('Mobile navigation route','/shop' in page.url and not page.locator('dialog').is_visible())
        for path in ['/shop','/product/foundation-hoodie','/bag','/checkout','/about','/lookbook','/guide','/design-system','/support/privacy','/missing']:
            route(path);record('Mobile layout '+path,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        route('/product/foundation-hoodie');record('Mobile purchase bar',page.locator('.mobile-purchase').is_visible())
        page.get_by_role('button',name='Search the collection',exact=True).click()
        page.keyboard.press('Tab');record('Dialog keyboard containment',page.evaluate('document.querySelector("dialog").contains(document.activeElement)'))
        page.keyboard.press('Escape')
        page.emulate_media(reduced_motion='reduce');record('Reduced motion styling',page.locator('.btn').first.evaluate('(el)=>parseFloat(getComputedStyle(el).transitionDuration)<0.01'))
        record('No JavaScript runtime errors',not errors,repr(errors))
        record('No external network requests',not [u for u in requests if u.startswith(('http:','https:'))],str(requests[:3]))
        # Explicitly mocked localStorage fixtures test validation, not browser persistence.
        fixtures=[({'bad':'shape'},0),([{'id':'missing','size':'M','colour':'Washed black','qty':1}],0),([{'id':'foundation-hoodie','size':'M','colour':'Washed black','qty':999}],7),([{'id':'foundation-hoodie','size':'XL','colour':'Washed black','qty':1}],0)]
        for idx,(value,expected) in enumerate(fixtures):
            pp=browser.new_page(viewport={'width':1440,'height':900})
            mock=f'<script>Object.defineProperty(window,"localStorage",{{value:{{getItem:()=>{json.dumps(json.dumps(value))},setItem:()=>{{}}}},configurable:true}});</script>'
            pp.set_content(html.replace('<body>','<body>'+mock),wait_until='load')
            count=pp.locator('.bag-count').inner_text();record(f'Basket fixture validation {idx+1}',count==f'({expected})',count);pp.close()
        browser.close()
    report={'environment':'Headless Chromium; standalone HTML injected locally without navigation. No external network. localStorage sanitisation fixtures are mocked; cross-session browser persistence not certified.','checks':len(RESULTS),'passed':sum(r['passed'] for r in RESULTS),'results':RESULTS,'not_tested':['Safari, Firefox and actual mobile hardware','Screen-reader testing or formal accessibility conformance','Live payment, inventory or fulfilment integrations','Production image quality or product-data accuracy','User research or customer usability validation']}
    (ROOT/'docs/qa-results.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({'checks':report['checks'],'passed':report['passed']},indent=2))
if __name__=='__main__':run()

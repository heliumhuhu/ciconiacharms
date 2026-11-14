"""Chromium integration and time-sampled geometry checks for 1.6.1."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os,json
URL=os.environ.get('CHARMS_TEST_URL','http://localhost:3000')
OUT=Path('/tmp/charms-validation');OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 errors=[]
 rack_code=(Path(__file__).resolve().parents[1]/'public/rack.js').read_text().replace('return {focus(id', 'window.__framing={boxes,render};return {focus(id')
 for width in [1440,768,390]:
  page=b.new_page(viewport={'width':width,'height':900},reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/rack.js',lambda route:route.fulfill(body=rack_code,content_type='text/javascript'))
  page.goto(URL);page.wait_for_function('charmsState().boxes===24');page.wait_for_timeout(500)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not page.locator('#save-target').is_visible()
  assert not page.locator('#description').is_visible()
  assert page.locator('#product-dialog').count()==0
  assert page.locator('.preview #save-target').count()==1
  page.screenshot(path=str(OUT/f'browse-{width}.png'),full_page=True)
  initial=page.evaluate('charmsState()');page.click('#preview-image');page.wait_for_function('charmsState().view?.phase==="ready"',timeout=15000)
  state=page.evaluate('charmsState()');identity=state['view']['cartonId'];r=page.locator('#scene').bounding_box();bounds=state['view']['bounds']
  assert min(v['y'] for v in bounds)>r['y']+5,(width,bounds,r)
  assert max(v['y'] for v in bounds)<r['y']+r['height']-5
  assert min(v['x'] for v in bounds)>=r['x'],(width,bounds,r)
  assert max(v['x'] for v in bounds)<=r['x']+r['width']
  for swing in [-.14,0,.14]:
   page.evaluate('(s)=>{__framing.boxes[0].userData.pivot.rotation.z=s;__framing.render()}',swing)
   points=page.evaluate('charmsState().view.bounds');assert all(r['x']<=p['x']<=r['x']+r['width'] and r['y']+5<p['y']<r['y']+r['height']-5 for p in points),(width,swing,points)
  page.evaluate('()=>{__framing.boxes[0].userData.pivot.rotation.z=0;__framing.render()}')
  page.screenshot(path=str(OUT/f'focus-{width}.png'),full_page=True)
  assert page.evaluate('charmsState().view.surroundingsVisible')==0
  page.evaluate("()=>{window.rewardCalls=0;const original=Element.prototype.animate;Element.prototype.animate=function(...a){if(this.id==='save-reward')rewardCalls++;return original.apply(this,a)}}")
  for _ in range(5):page.click('#saved-plus')
  assert page.evaluate('charmsState().total')==5
  assert '5' in page.locator('#saved-total').inner_text()
  assert page.evaluate('rewardCalls')==5
  page.click('#focus-undo');assert page.evaluate('charmsState().total')==4
  page.reload();page.wait_for_function('charmsState().boxes===24');assert page.evaluate('charmsState().total')==4
  page.click('#preview-image');page.wait_for_function('charmsState().view?.phase==="ready"')
  page.evaluate("localStorage.clear()")
  page.reload();page.wait_for_function('charmsState().boxes===24');page.click('#preview-image');page.wait_for_function('charmsState().view?.phase==="ready"')
  identity=page.evaluate('charmsState().view.cartonId')
  # Reposition after controls scroll the viewport.
  page.locator('#scene').scroll_into_view_if_needed();v=page.evaluate('charmsState().view.center');target=page.locator('#save-target').bounding_box();end={'x':target['x']+target['width']/2,'y':target['y']+30}
  page.mouse.move(v['x'],v['y']);page.mouse.down();page.mouse.move(end['x'],end['y'],steps=12)
  assert page.evaluate('charmsState().view.dragging')
  assert page.evaluate('charmsState().view.anchorError')<1e-6
  page.screenshot(path=str(OUT/f'drag-{width}.png'))
  page.mouse.up();assert page.evaluate('charmsState().total')==1
  samples=[]
  for i in range(5):
   samples.append(page.evaluate('charmsState().view'));page.wait_for_timeout(100)
  page.wait_for_function('charmsState().view.phase==="ready"',timeout=15000)
  assert page.evaluate('charmsState().view.cartonId')==identity
  assert page.evaluate('charmsState().view.attached')
  (OUT/f'return-{width}.json').write_text(json.dumps(samples,indent=2))
  # Repeat a valid drag in the same focus; Undo removes only its one unit.
  v=page.evaluate('charmsState().view.center');page.mouse.move(v['x'],v['y']);page.mouse.down();page.mouse.move(end['x'],end['y'],steps=8);page.mouse.up();assert page.evaluate('charmsState().total')==2
  page.wait_for_function('charmsState().view.phase==="ready"',timeout=15000);page.click('#focus-undo');assert page.evaluate('charmsState().total')==1
  page.locator('#scene').scroll_into_view_if_needed();v=page.evaluate('charmsState().view.center');target=page.locator('#save-target').bounding_box();end={'x':target['x']+target['width']/2,'y':target['y']+30}
  page.mouse.move(v['x'],v['y']);page.mouse.down();page.mouse.move(end['x'],end['y'],steps=8);page.locator('#scene').dispatch_event('pointercancel',{'pointerId':1});page.mouse.up();page.wait_for_function('charmsState().view.phase==="ready"',timeout=15000);assert page.evaluate('charmsState().total')==1
  # Cancellation while over the target adds nothing.
  v=page.evaluate('charmsState().view.center');page.mouse.move(v['x'],v['y']);page.mouse.down();page.mouse.move(end['x'],end['y'],steps=8);page.keyboard.press('Escape');page.mouse.up()
  page.wait_for_function('!charmsState().focus',timeout=15000)
  assert page.evaluate('charmsState().total')==1
  assert abs(page.evaluate('charmsState().angle')-initial['angle'])<1e-9
  assert not page.locator('#save-target').is_visible()
  page.reload();page.wait_for_function('charmsState().boxes===24');assert page.evaluate('charmsState().total')==1
  # Exact list selection, description search, no-results/reset, opposite packaging.
  page.locator('#list-view').evaluate('(e)=>e.open=true');page.fill('#list-search','description17');assert page.locator('.list-product').count()==1
  page.click('.list-product');page.wait_for_function('charmsState().view?.phase==="ready"',timeout=15000);assert page.evaluate('charmsState().focus')=='product-17'
  r=page.locator('#scene').bounding_box()
  for swing in [-.14,0,.14]:
   page.evaluate('(s)=>{__framing.boxes[16].userData.pivot.rotation.z=s;__framing.render()}',swing)
   points=page.evaluate('charmsState().view.bounds');assert all(r['x']<=p['x']<=r['x']+r['width'] and r['y']+5<p['y']<r['y']+r['height']-5 for p in points),(width,swing,points)
  page.evaluate('()=>{__framing.boxes[16].userData.pivot.rotation.z=0;__framing.render()}')
  page.screenshot(path=str(OUT/f'toy-{width}.png'),full_page=True)
  bounds=page.evaluate('charmsState().view.bounds');r=page.locator('#scene').bounding_box();assert min(v['y'] for v in bounds)>r['y'];assert max(v['y'] for v in bounds)<r['y']+r['height']
  page.click('#back');page.wait_for_function('!charmsState().focus',timeout=15000)
  page.fill('#list-search','no such item');assert page.locator('#list-empty').is_visible();page.click('#list-reset');assert page.locator('.list-product').count()==24
  print('PASS viewport',width,flush=True);page.close()
 assert not errors,errors
 b.close()

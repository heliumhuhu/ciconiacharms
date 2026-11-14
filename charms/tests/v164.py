from playwright.sync_api import sync_playwright
from pathlib import Path
import json
out=Path('/tmp/charms-v164');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 for width in [390,768,1440]:
  page=b.new_page(viewport={'width':width,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://localhost:3000');page.wait_for_function('charmsState().boxes===24')
  # Background wheel event passes through; carton wheel retains momentum after quiet.
  page.locator('#scene').scroll_into_view_if_needed();r=page.locator('#scene').bounding_box();before=page.evaluate('charmsState().angle')
  page.locator('#scene').dispatch_event('wheel',{'clientX':r['x']+2,'clientY':r['y']+2,'deltaY':90});page.wait_for_timeout(200);assert page.evaluate('charmsState().angle')==before
  center=page.evaluate('charmsState().centers.find(c=>c.id===charmsState().front)')
  samples=page.evaluate("""async c=>{const samples=[];document.querySelector('#scene').dispatchEvent(new WheelEvent('wheel',{clientX:c.x,clientY:c.y,deltaY:90,bubbles:true,cancelable:true}));await new Promise(resolve=>{function sample(){const s=charmsState();samples.push({angle:s.angle,state:s.state});if(s.state==='idle')resolve();else requestAnimationFrame(sample)}requestAnimationFrame(sample)});return samples}""",center)
  assert all(s['state']!='coasting' for s in samples),samples
  assert samples[-1]['state']=='idle' and any(s['state']=='settling' for s in samples),samples
  (out/f'momentum-{width}.json').write_text(json.dumps(samples))
  # Inspect animation synchronously to avoid automation latency skipping its duration.
  for opening in [True,False]:
   result=page.evaluate("""async ()=>{const d=document.querySelector('#list-view');d.querySelector('summary').click();const a=d.getAnimations()[0],during={open:d.open,animated:!!a,ripples:[...document.querySelectorAll('.list-product')].map(x=>x.getAnimations().map(a=>a.effect.getTiming().delay)).flat()};if(a)await a.finished;await new Promise(requestAnimationFrame);return {...during,after:d.open}}""")
   assert result['open'] and result['animated'] and result['after']==opening,result
   assert (len(result['ripples'])==24 and max(result['ripples'])>min(result['ripples'])) if opening else not result['ripples'],result
  page.click('#preview-image');page.wait_for_function('charmsState().view?.phase==="ready"')
  r=page.locator('#scene').bounding_box();bounds=page.evaluate('charmsState().view.bounds');assert all(r['x']<=q['x']<=r['x']+r['width'] and r['y']<=q['y']<=r['y']+r['height'] for q in bounds),(width,bounds,r)
  assert page.locator('#preview-image').bounding_box()['height']>=280
  assert page.locator('#detail-add').count()==0
  for _ in range(5):page.click('#saved-plus')
  assert page.locator('#saved-total').inner_text()=='5';assert page.evaluate('charmsState().total')==5
  page.click('#saved-minus');assert page.locator('#saved-total').inner_text()=='4'
  page.click('#saved-plus');page.click('#focus-undo');assert page.evaluate('charmsState().total')==4
  for _ in range(4):page.click('#saved-minus')
  assert page.locator('#saved-minus').is_disabled();assert page.locator('#saved-total').inner_text()=='0'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.locator('#scene').scroll_into_view_if_needed();page.screenshot(path=str(out/f'focus-{width}.png'),full_page=True)
  page.keyboard.press('Escape');page.wait_for_function('!charmsState().focus');assert not errors,errors
  print('PASS restored physics and ripple viewport',width,flush=True);page.close()
 b.close()

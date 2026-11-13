"""Frame samples, same-object recovery and interrupted phases for v1.6.1."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os
OUT=Path('/tmp/charms-validation');OUT.mkdir(exist_ok=True)
URL=os.environ.get('CHARMS_TEST_URL','http://localhost:3000')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 page=b.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 # Observe the exact zero-scale relocation boundary, without replacing mechanics.
 source=(Path(__file__).resolve().parents[1]/'public/product-view.js').read_text()
 source=source.replace('carton.visible=false;carton.scale.copy(homeScale);parent.attach(carton);', 'window.__relocations.push({scale:carton.scale.x,phase});carton.visible=false;carton.scale.copy(homeScale);parent.attach(carton);')
 page.route('**/product-view.js',lambda r:r.fulfill(body=source,content_type='text/javascript'))
 page.goto(URL);page.wait_for_function('charmsState().boxes===24');page.evaluate('window.__relocations=[]')
 initial=page.evaluate('charmsState()')
 def open_focus():
  page.locator('#preview-image').click();page.wait_for_function('charmsState().view?.phase==="ready"',timeout=30000)
 def drag(valid=True):
  page.locator('#scene').scroll_into_view_if_needed();v=page.evaluate('charmsState().view.center');r=page.locator('#save-target').bounding_box()
  page.mouse.move(v['x']+12,v['y']+12);page.mouse.down();assert page.evaluate('charmsState().view.dragging')
  page.mouse.move(r['x']+r['width']/2 if valid else v['x']+40,r['y']+25 if valid else v['y']+20,steps=5)
  assert page.evaluate('charmsState().view.anchorError')<1e-6
 def watch(escape_phase=None):
  page.evaluate('''phase=>{window.__samples=[];window.__escapePhase=phase;
   function sample(){const s=charmsState();if(!s.view)return;__samples.push({...s.view,total:s.total,buttonDisabled:document.querySelector("#detail-add").disabled});
    if(s.view.phase===__escapePhase){__escapePhase=null;document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));}
    if(s.view.phase!=='ready')requestAnimationFrame(sample);
   }requestAnimationFrame(sample)}''',escape_phase)
 open_focus();home=page.evaluate('charmsState().view');assert home['blurredGroups']==0 and home['sharpHook']
 r=page.locator('#scene').bounding_box();back=page.locator('#back').bounding_box();assert back['y']+back['height']<=r['y']
 drag();watch();page.mouse.up();assert page.evaluate('charmsState().total')==1
 page.wait_for_function('charmsState().view.phase==="ready"',timeout=30000)
 samples=page.evaluate('__samples');(OUT/'save-sequence.json').write_text(json.dumps(samples,indent=2))
 phases={s['phase'] for s in samples};assert {'disappearing','reappearing'}<=phases,phases
 assert all(s['cartonId']==home['cartonId'] for s in samples)
 assert all(s['buttonDisabled'] for s in samples if s['phase'] in ['disappearing','reappearing'])
 assert all(s['total']==1 for s in samples if s['phase'] in ['disappearing','reappearing'])
 assert all(not s['attached'] for s in samples if s['phase']=='disappearing')
 assert all(s['attached'] for s in samples if s['phase']=='reappearing')
 assert page.evaluate('__relocations')==[{'scale':0,'phase':'disappearing'}]
 assert all(max(abs(a-b) for a,b in zip(s['position'],next(v for v in samples if v['phase']=='disappearing')['position']))<1e-6 for s in samples if s['phase']=='disappearing')
 assert page.evaluate('charmsState().view.scale')==1
 # Repeated completed additions and latest-action Undo preserve the earlier unit.
 page.click('#quantity-plus');page.click('#detail-add');assert page.evaluate('charmsState().total')==3
 page.click('#focus-undo');assert page.evaluate('charmsState().total')==1
 page.click('#back');page.wait_for_function('!charmsState().focus',timeout=30000)
 for phase in ['dragging','disappearing','reappearing','returning']:
  open_focus();drag(phase!='returning');before=page.evaluate('charmsState().total')
  if phase=='dragging':page.keyboard.press('Escape');page.mouse.up();expected=before
  else:
   watch(phase);page.mouse.up();expected=before+(phase!='returning')
  page.wait_for_function('!charmsState().focus',timeout=30000)
  state=page.evaluate('charmsState()');assert state['total']==expected,(phase,state)
  assert state['angle']==initial['angle'] and state['camera']==initial['camera']
  open_focus();v=page.evaluate('charmsState().view');assert v['attached'] and v['scale']==1 and v['visible']
  assert v['cartonId']==home['cartonId'];page.keyboard.press('Escape');page.wait_for_function('!charmsState().focus',timeout=30000)
  print('PASS interruption',phase,flush=True)
 assert not errors,errors
 print('PASS zero-scale relocation, frame sequence, one object, precise pivot, exact quantities, Undo, sharp hook and no blur groups',flush=True)
 b.close()

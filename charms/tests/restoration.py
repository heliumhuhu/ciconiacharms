"""Material/visibility restoration and stable idle canvas after focus."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 page=b.new_page(viewport={'width':390,'height':900})
 code=(Path(__file__).resolve().parents[1]/'public/rack.js').read_text().replace('return {focus(id','window.__scene=scene;return {focus(id')
 page.route('**/rack.js',lambda r:r.fulfill(body=code,content_type='text/javascript'))
 page.goto(os.environ.get('CHARMS_TEST_URL','http://localhost:3000'));page.wait_for_function('charmsState().boxes===24')
 snapshot="""()=>{const result=[];__scene.traverse(o=>{if(o.isMesh)result.push([o.uuid,o.visible,...(Array.isArray(o.material)?o.material:[o.material]).map(m=>m.uuid)])});return result}"""
 before=page.evaluate(snapshot)
 page.click('#preview-image');page.wait_for_function('charmsState().view?.phase==="ready"')
 assert page.evaluate('charmsState().view.surroundingsVisible')==0
 assert page.evaluate("document.querySelector('canvas').getBoundingClientRect().height===document.querySelector('#scene').clientHeight")
 page.keyboard.press('Escape');page.wait_for_function('!charmsState().focus')
 assert page.evaluate(snapshot)==before
 page.screenshot(path='/tmp/charms-validation/restored-390.png',full_page=True)
 print('PASS exact material/mesh visibility restoration and scene-sized idle canvas',flush=True)
 b.close()

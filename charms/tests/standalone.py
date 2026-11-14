from playwright.sync_api import sync_playwright
from pathlib import Path
release=Path(__file__).resolve().parents[2]/'CICONIA-CHARMS-v1.6.5.html'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 for mode in ['embedded','file','fallback']:
  context=b.new_context(offline=True,viewport={'width':1440,'height':900});page=context.new_page();network=[];errors=[]
  page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None);page.on('pageerror',lambda e:errors.append(str(e)))
  if mode=='fallback':page.evaluate("()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t,...a){return t.includes('webgl')?null:original.call(this,t,...a)}}")
  if mode in ['embedded','fallback']:page.set_content(release.read_text(),wait_until='load')
  else:
   try:page.goto(release.as_uri())
   except Exception as e:print('BLOCKED file navigation',str(e));context.close();continue
  page.wait_for_function('window.charmsState')
  if mode!='fallback':page.wait_for_function('charmsState().boxes===24')
  page.click('#preview-image')
  if mode!='fallback':page.wait_for_function('charmsState().view?.phase==="ready"',timeout=15000)
  page.evaluate('''()=>{window.rewards=0;const original=Element.prototype.animate;Element.prototype.animate=function(...args){if(this.id==='save-reward')rewards++;return original.apply(this,args)};for(let i=0;i<20;i++)document.querySelector('#saved-plus').click()}''')
  assert page.evaluate('charmsState().total')==20
  assert page.evaluate('rewards')==20
  assert '20' in page.locator('#saved-total').inner_text()
  assert page.locator('#save-reward').count()==1
  assert page.evaluate("document.querySelector('#save-reward').getAnimations().length")<=1
  page.wait_for_timeout(800);assert page.evaluate('charmsState().total')==20
  page.click('#focus-undo');assert page.evaluate('charmsState().total')==19
  page.keyboard.press('Escape');page.wait_for_function('!charmsState().focus',timeout=15000)
  assert not errors,errors;assert not network,network
  print('PASS offline',mode,flush=True);context.close()
 b.close()

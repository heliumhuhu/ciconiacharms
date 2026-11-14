from playwright.sync_api import sync_playwright
from pathlib import Path
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.add_init_script("const get=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t,...a){return t.includes('webgl')?null:get.call(this,t,...a)}")
 page.goto('http://localhost:3000');page.wait_for_function('window.charmsState')
 page.evaluate("document.querySelector('#list-view').open=false")
 page.locator('#list-view summary').focus();page.keyboard.press('Enter')
 samples=page.evaluate("""()=>{const d=document.querySelector('#list-view');d.getAnimations().forEach(a=>{a.pause();a.currentTime=320});return [...document.querySelectorAll('.list-product')].map(e=>{const a=e.getAnimations()[0];if(!a)return null;a.pause();a.currentTime=220;return {delay:a.effect.getTiming().delay,opacity:getComputedStyle(e).opacity}})}""")
 assert len(samples)==24 and all(samples),samples
 assert float(samples[0]['opacity'])>float(samples[3]['opacity']),samples[:4]
 Path('/tmp/charms-v165').mkdir(exist_ok=True)
 page.screenshot(path='/tmp/charms-v165/ripple.png')
 result=page.evaluate("""async ()=>{const d=document.querySelector('#list-view'),s=d.querySelector('summary');s.click();const cancelled=[...document.querySelectorAll('.list-product')].every(e=>!e.getAnimations().length);s.click();const restarted=[...document.querySelectorAll('.list-product')].every(e=>e.getAnimations().length===1);await Promise.all(d.getAnimations().map(a=>a.finished));await new Promise(requestAnimationFrame);return {cancelled,restarted,open:d.open}}""")
 assert result=={'cancelled':True,'restarted':True,'open':True},result
 assert not errors,errors
 print('PASS keyboard expansion, sampled ripple opacity, collapse cancellation and rapid reversal')
 b.close()

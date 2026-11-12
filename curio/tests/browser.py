from playwright.sync_api import sync_playwright,expect
import os
URL=os.environ.get('CURIO_TEST_URL','http://127.0.0.1:3000')
def settled(page):
 page.wait_for_function('curioState().state === "idle"',timeout=5000)
def state(page):return page.evaluate('curioState()')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 for width in [1440,768,390]:
  page=browser.new_page(viewport={'width':width,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(URL);page.wait_for_function('window.curioState && curioState().boxes===24')
  initial=state(page);camera=initial['camera']
  geometry=page.evaluate('curioGeometry()');assert len(geometry)==24;assert all(g['slotMargin']>0 and -.001<g['railClearance']<.002 and g['attachmentError']<.005 for g in geometry);assert len({g['color'] for g in geometry if g['category']=='toys'})==1;assert len({g['color'] for g in geometry if g['category']=='jewellery'})==1;assert len({g['color'] for g in geometry})==2
  page.locator('[data-category=toys]').click();settled(page);assert state(page)['front']=='product-19';assert state(page)['boxes']==24;assert state(page)['camera']==camera
  page.locator('[data-category=jewellery]').click();settled(page);assert state(page)['front']=='product-7'
  page.locator('#scene').focus();page.keyboard.press('ArrowRight');settled(page);assert state(page)['front']=='product-8';assert state(page)['preview']=='product-8'
  # Drag stays free while held; hold after movement is an ordinary drag release.
  box=page.locator('#scene').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.55
  page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+32,y,steps=4);page.wait_for_timeout(300);assert state(page)['state']=='dragging';a=state(page)['angle'];page.wait_for_timeout(200);assert abs(state(page)['angle']-a)<1e-9;page.mouse.up();settled(page)
  # Stationary hold suppresses opening and snapping; movement after a hold resumes.
  page.mouse.move(x,y);page.mouse.down();page.wait_for_timeout(320);a=state(page)['angle'];assert state(page)['state']=='held';page.mouse.up();page.wait_for_timeout(450);assert abs(state(page)['angle']-a)<1e-9;assert not state(page)['focus']
  page.mouse.down();page.wait_for_timeout(300);page.mouse.move(x+35,y,steps=3);assert state(page)['state']=='dragging';page.mouse.up();settled(page)
  # Wheel input cancels a settle and settles only after quiet.
  page.mouse.move(x,y);page.mouse.wheel(0,80);page.wait_for_timeout(60);page.mouse.wheel(0,40);page.wait_for_timeout(250);settled(page)
  assert not errors,errors
  print('PASS browsing motion',width,flush=True)
  page.close()
 browser.close()

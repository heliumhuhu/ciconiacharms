"""Integrated fallback UI: independent catalogue, quantities and storage edges."""
from playwright.sync_api import sync_playwright
import os
URL=os.environ.get('CHARMS_TEST_URL','http://localhost:3000')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.add_init_script('''const get=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t,...a){return t.includes('webgl')?null:get.call(this,t,...a)};
 localStorage.setItem('ciconia-charms-quantities',JSON.stringify({'product-1':998,'retired-product':2}));''')
 page.goto(URL);page.wait_for_function('window.charmsState');assert page.evaluate('charmsState().total')==1000
 assert not page.locator('#save-target').is_visible()
 assert page.locator('.list-product').count()==24
 page.select_option('#list-category','toys');page.fill('#list-search','description17');page.select_option('#list-sort','high')
 assert page.locator('.list-product').count()==1
 assert page.locator('#list-count').inner_text()=='1 of 24 products'
 assert page.locator('#price-note').is_visible();page.click('.list-product')
 assert page.evaluate('charmsState().focus')=='product-17';assert page.locator('.preview #save-target').count()==1
 assert '0' in page.locator('#saved-total').inner_text();page.click('#saved-plus');assert page.evaluate('charmsState().total')==1001
 page.click('#focus-undo');assert page.evaluate('charmsState().total')==1000
 page.keyboard.press('Escape');page.wait_for_function('!charmsState().focus')
 page.click('#list-reset');assert page.locator('.list-product').count()==24
 page.select_option('#list-category','jewellery');page.select_option('#list-sort','name');assert page.locator('.list-product').count()==12
 assert '[product1]' in page.locator('.list-product').first.inner_text()
 page.fill('#list-search','absent');assert page.locator('#list-empty').is_visible();page.click('#list-reset')
 page.locator('.list-product').first.click();page.click('#saved-plus')
 assert page.evaluate('charmsState().quantities["product-1"]')==999
 page.click('#focus-undo');assert page.evaluate('charmsState().quantities["product-1"]')==998
 page.keyboard.press('Escape');page.click('#my-box');assert page.get_by_text('Unavailable',exact=True).is_visible()
 assert page.get_by_role('button',name='Increase retired-product',exact=True).is_disabled()
 page.get_by_role('button',name='Remove retired-product',exact=True).click();assert page.evaluate('charmsState().total')==998
 assert not errors,errors;page.close()
 # Actual app with unavailable localStorage still works in memory.
 page=b.new_page();page.add_init_script('''Object.defineProperty(window,'localStorage',{get(){throw new Error('storage blocked')}});
 const get=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t,...a){return t.includes('webgl')?null:get.call(this,t,...a)};''')
 page.goto(URL);page.wait_for_function('window.charmsState');page.click('#preview-image');page.click('#saved-plus');assert page.evaluate('charmsState().total')==1
 print('PASS fallback, combined filters/sort/count/reset, exact identity, quantity cap, latest amount Undo, unavailable rows and blocked storage',flush=True)
 b.close()

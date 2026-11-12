from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=b.new_page(viewport={'width':1100,'height':850})
 code=(Path(__file__).resolve().parents[1]/'public/rack.js').read_text().replace('return {focus(id', 'window.__inspect={THREE,camera,scene,rack,get boxes(){return boxes},render};return {focus(id')
 page.route('**/rack.js',lambda route:route.fulfill(body=code,content_type='text/javascript'));page.goto('http://127.0.0.1:3000');page.wait_for_function('window.curioState && curioState().boxes===24')
 geometry=page.evaluate('curioGeometry()');assert all(g['slotMargin']>0 and -.001<g['railClearance']<.002 and g['attachmentError']<.005 for g in geometry);print('PASS hook contact, slot clearance and attachment; capturing front/side/rear swing views',flush=True)
 # Oriented bounding-box SAT on the actual carton meshes, all pairs at
 # both limits of the shared hanging-swing dynamics (not world AABBs).
 collisions=page.evaluate("""()=>{const v=window.__inspect,T=v.THREE,failures=[];
 function obb(b){const mesh=b.userData.pivot.children.find(c=>c.geometry?.type==='ExtrudeGeometry');mesh.geometry.computeBoundingBox();const bb=mesh.geometry.boundingBox,center=bb.getCenter(new T.Vector3()).applyMatrix4(mesh.matrixWorld),half=bb.getSize(new T.Vector3()).multiplyScalar(.5);return {center,half:half.toArray(),axes:[new T.Vector3(1,0,0),new T.Vector3(0,1,0),new T.Vector3(0,0,1)].map(a=>a.transformDirection(mesh.matrixWorld))}}
 function overlap(a,b){const delta=b.center.clone().sub(a.center),axes=[...a.axes,...b.axes,...a.axes.flatMap(x=>b.axes.map(y=>x.clone().cross(y)))];for(const axis of axes){if(axis.lengthSq()<1e-10)continue;axis.normalize();const radius=q=>q.axes.reduce((sum,x,i)=>sum+q.half[i]*Math.abs(axis.dot(x)),0);if(Math.abs(delta.dot(axis))>radius(a)+radius(b))return false}return true}
 for(const swing of [-.14,0,.14]){v.boxes.forEach(b=>b.userData.pivot.rotation.z=swing);v.rack.updateMatrixWorld(true);const bounds=v.boxes.map(obb);for(let i=0;i<bounds.length;i++)for(let j=i+1;j<bounds.length;j++)if(overlap(bounds[i],bounds[j]))failures.push([swing,i,j])}return failures}""")
 assert not collisions,collisions
 print('PASS no carton intersections through shared swing extremes',flush=True)
 for width in [390,768,1440]:
  page.set_viewport_size({'width':width,'height':900});page.wait_for_timeout(250)
  framed=page.evaluate("""()=>{const v=window.__inspect,T=v.THREE,r=document.querySelector('#scene').getBoundingClientRect(),errors=[];for(const swing of [-.14,0,.14]){v.boxes[0].userData.pivot.rotation.z=swing;v.render();const box=new T.Box3().setFromObject(v.boxes[0].userData.pivot);for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z]){const q=new T.Vector3(x,y,z).project(v.camera);if(Math.abs(q.y)>.98||Math.abs(q.x)>1)errors.push(q.toArray())}}return errors}""")
  assert not framed,(width,framed)
 print('PASS full browsing carton bounds at all viewport widths and permitted swing extremes',flush=True)
 for name,x,z,swing in [('front',0,1.5,0),('side',1.5,.05,.14),('rear',0,-1.5,-.14)]:
  page.evaluate('''([x,z,swing])=>{const v=window.__inspect,b=v.boxes[0];v.boxes.forEach(o=>o.visible=o===b);b.userData.pivot.rotation.z=swing;v.rack.updateMatrixWorld(true);const point=b.position.clone();point.set(0,1.422,-.1355);b.localToWorld(point);const offset=point.clone().set(x,0,z);offset.applyAxisAngle({x:0,y:1,z:0},b.rotation.y+v.rack.rotation.y);v.camera.position.copy(point).add(offset);v.camera.fov=32;v.camera.lookAt(point.x,point.y-.04,point.z);v.camera.updateProjectionMatrix();v.render()}''',[x,z,swing]);page.locator('#scene').screenshot(path=f'/tmp/hook-{name}.png')
 b.close()

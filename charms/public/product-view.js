import * as THREE from '/vendor/three.module.js';
// One renderer, one carton. Reparenting preserves the world transform.
export function createProductView(c){
 const {sceneHost:host,scene,camera,carton,group,render,onSave,onBusy}=c;
 const parent=carton.parent,home=carton.position.clone(),homeQ=carton.quaternion.clone(),savedAngle=c.angle();
 // One sharp scene. Layers only extend the actual dragged carton over the card.
 const layerMasks=new Map();scene.traverse(o=>layerMasks.set(o,o.layers.mask));
 const lights=[];scene.traverse(o=>{if(o.isLight){lights.push([o,o.layers.mask]);o.layers.enableAll()}});
 function renderScene(renderer){
  const w=host.clientWidth,h=host.clientHeight,showroom=host.closest('.showroom'),expanded=!!(drag||returning||saveAnimation),fullW=expanded?showroom.clientWidth:w,fullH=expanded?showroom.clientHeight:h;
  camera.setViewOffset(w,h,0,0,fullW,fullH);
  const size=renderer.getSize(new THREE.Vector2());if(size.x!==fullW||size.y!==fullH)renderer.setSize(fullW,fullH,false);
  renderer.domElement.style.width=fullW+'px';renderer.domElement.style.height=fullH+'px';
  const mask=camera.layers.mask;camera.layers.enableAll();renderer.clear();
  renderer.setScissorTest(true);renderer.setScissor(0,fullH-h,w,h);renderer.render(scene,camera);renderer.setScissorTest(false);
  if(drag||returning||phase==='disappearing'){renderer.autoClear=false;renderer.clearDepth();camera.layers.set(1);renderer.render(scene,camera);renderer.autoClear=true;}
  camera.layers.mask=mask;
 }
 carton.traverse(o=>o.layers.set(1));group.children.filter(o=>o!==carton).forEach(o=>o.traverse(n=>n.layers.set(1)));
 // Clone only materials: shared rack materials must not fade the selected carton.
 const faded=[];
 scene.traverse(o=>{if(!o.isMesh||!o.material)return;let selected=false;for(let n=o;n;n=n.parent)if(n===group)selected=true;if(selected)return;
 const original=o.material,materials=(Array.isArray(original)?original:[original]).map(m=>{const copy=m.clone();copy.transparent=true;return copy});
 faded.push({o,original,materials,opacity:materials.map(m=>m.opacity),visible:o.visible});o.material=Array.isArray(original)?materials:materials[0];
 });
 function fadeSurroundings(k){for(const f of faded){f.o.visible=f.visible&&k<1;f.materials.forEach((m,i)=>{m.opacity=f.opacity[i]*(1-k);m.depthWrite=k===0})}}
 const target=document.querySelector('#save-target'),label=document.querySelector('#target-instruction');
 const anchor=new THREE.Group();scene.add(anchor);
 const ray=new THREE.Raycaster();ray.layers.set(1);const pointer=new THREE.Vector2(),plane=new THREE.Plane(),point=new THREE.Vector3();
 const homeScale=carton.scale.clone();
 let phase='zooming',drag=null,returning=null,saveAnimation=null,leaving=false,done=null,frame=0,last=performance.now(),velocity=0,desired=0,progress=0;
 const startCamera=camera.position.clone();c.cameraLayout(true);const focusCamera=camera.position.clone();camera.position.copy(startCamera);
 const ease=t=>t*t*(3-2*t);
 function setPhase(p){phase=p;host.dataset.phase=p;onBusy(p!=='ready')}
 function project(e){const r=c.renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);ray.setFromCamera(pointer,camera)}
 function over(e){const r=target.getBoundingClientRect();return e.clientX>=r.left&&e.clientX<=r.right&&e.clientY>=r.top&&e.clientY<=r.bottom}
 function request(){if(!frame)frame=requestAnimationFrame(tick)}
 function tick(now){frame=0;const dt=Math.min(.1,(now-last)/1000);last=now;
  if(phase==='zooming'||leaving){progress=Math.max(0,Math.min(1,progress+(leaving?-1:1)*dt/.65));const k=ease(progress);fadeSurroundings(k);camera.position.lerpVectors(startCamera,focusCamera,k);camera.lookAt(0,.34,3.4);c.setAngle(savedAngle+(c.goal-savedAngle)*k);if(progress===1&&!leaving)setPhase('ready');}
  if(drag){desired*=Math.exp(-6*dt);velocity+=(desired-anchor.rotation.z)*65*dt-velocity*9*dt;anchor.rotation.z+=velocity*dt;}
  if(saveAnimation){
   saveAnimation.t=Math.min(1,saveAnimation.t+dt/.24);const k=ease(saveAnimation.t);
   carton.scale.copy(homeScale).multiplyScalar(phase==='disappearing'?1-k:k);
   if(saveAnimation.t===1){if(phase==='disappearing'){
    // Zero scale is reached before relocation; never travel visibly home.
    carton.visible=false;carton.scale.copy(homeScale);parent.attach(carton);carton.position.copy(home);carton.quaternion.copy(homeQ);carton.scale.setScalar(0);
    saveAnimation.t=0;setPhase('reappearing');carton.visible=true;
   }else{carton.scale.copy(homeScale);saveAnimation=null;host.classList.remove('returning');setPhase(leaving?'leaving':'ready')}}
  }
  if(returning){returning.t=Math.min(1,returning.t+dt/.65);const k=ease(returning.t);parent.updateWorldMatrix(true,false);const destination=parent.localToWorld(home.clone()),q=parent.getWorldQuaternion(new THREE.Quaternion()).multiply(homeQ);carton.position.lerpVectors(returning.from,destination,k);carton.position.y+=Math.sin(Math.PI*k)*.12;carton.quaternion.slerpQuaternions(returning.q,q,k);if(returning.t===1){parent.attach(carton);carton.position.copy(home);carton.quaternion.copy(homeQ);returning=null;setPhase(leaving?'leaving':'settling');settleStart=now;}}
  if(phase==='settling'){const t=(now-settleStart)/1000;carton.quaternion.copy(homeQ);carton.rotateZ(Math.sin(t*18)*.025*Math.exp(-t*9));if(t>.45){carton.quaternion.copy(homeQ);setPhase('ready');host.classList.remove('returning');}}
  render();
  if(leaving&&progress===0&&!returning&&!saveAnimation){cleanup();c.onDone();done?.();return}
  if(phase!=='ready'||drag||leaving)request();
 }
 let settleStart=0;
 function reset(){scene.attach(carton);returning={from:carton.position.clone(),q:carton.quaternion.clone(),t:0};host.classList.remove('dragging','over-target');host.classList.add('returning');label.textContent='Drag here to add to My box';setPhase(leaving?'leaving':'returning');request()}
 function down(e){if(phase!=='ready'||leaving||e.button!==0||e.target.closest('button'))return;project(e);const hit=ray.intersectObject(carton,true)[0];if(!hit)return;const local=carton.worldToLocal(hit.point.clone());anchor.position.copy(hit.point);anchor.quaternion.identity();anchor.attach(carton);plane.setFromNormalAndCoplanarPoint(camera.getWorldDirection(new THREE.Vector3()),hit.point);drag={id:e.pointerId,x:e.clientX,y:e.clientY,lastX:e.clientX,local,planeConstant:plane.constant,moved:false};velocity=desired=0;last=performance.now();setPhase('dragging');host.classList.add('dragging');host.setPointerCapture(e.pointerId);request()}
 function move(e){if(!drag||e.pointerId!==drag.id)return;project(e);plane.constant=drag.planeConstant+Math.min(.24,Math.hypot(e.clientX-drag.x,e.clientY-drag.y)*.006);if(ray.ray.intersectPlane(plane,point))anchor.position.copy(point);drag.moved ||= Math.hypot(e.clientX-drag.x,e.clientY-drag.y)>8;desired=THREE.MathUtils.clamp(-(e.clientX-drag.lastX)*.008,-.12,.12);drag.lastX=e.clientX;const valid=over(e);host.classList.toggle('over-target',valid);label.textContent=valid?'Release to add to My box':'Drag here to add to My box';render()}
 function release(e,cancel=false){if(!drag||e.pointerId!==drag.id)return;const valid=!cancel&&drag.moved&&over(e);drag=null;if(host.hasPointerCapture(e.pointerId))host.releasePointerCapture(e.pointerId);if(valid&&onSave()){saveAnimation={t:0};host.classList.remove('dragging','over-target');host.classList.add('returning');label.textContent='Drag here to add to My box';setPhase('disappearing');request()}else reset()}
 const up=e=>release(e),cancel=e=>release(e,true);
 host.addEventListener('pointerdown',down);host.addEventListener('pointermove',move);host.addEventListener('pointerup',up);host.addEventListener('pointercancel',cancel);host.addEventListener('lostpointercapture',cancel);
 function cleanup(){for(const f of faded){f.o.material=f.original;f.o.visible=f.visible;f.materials.forEach(m=>m.dispose())}for(const [o,mask] of layerMasks)o.layers.mask=mask;for(const [o,mask] of lights)o.layers.mask=mask;carton.quaternion.copy(homeQ);carton.scale.copy(homeScale);carton.visible=true;cancelAnimationFrame(frame);host.removeEventListener('pointerdown',down);host.removeEventListener('pointermove',move);host.removeEventListener('pointerup',up);host.removeEventListener('pointercancel',cancel);host.removeEventListener('lostpointercapture',cancel);scene.remove(anchor);host.classList.remove('dragging','returning','over-target');delete host.dataset.phase;c.cameraLayout(false);c.renderer.setSize(host.clientWidth,host.clientHeight);}
 setPhase('zooming');request();
 return {renderScene,leave(callback){if(leaving)return;leaving=true;last=performance.now();done=callback;if(drag)cancel({pointerId:drag.id});if(!saveAnimation)setPhase('leaving');request()},resize(){c.cameraLayout(false);startCamera.copy(camera.position);c.cameraLayout(true);focusCamera.copy(camera.position);camera.position.lerpVectors(startCamera,focusCamera,ease(progress));if(drag)cancel({pointerId:drag.id});render()},diagnostics(){scene.updateMatrixWorld(true);const bounds=new THREE.Box3().setFromObject(carton),r=c.renderer.domElement.getBoundingClientRect(),points=[];for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){const v=new THREE.Vector3(x,y,z).project(camera);points.push({x:r.left+(v.x+1)*r.width/2,y:r.top+(1-v.y)*r.height/2})}const v=bounds.getCenter(new THREE.Vector3()).project(camera);return {phase,center:{x:r.left+(v.x+1)*r.width/2,y:r.top+(1-v.y)*r.height/2},bounds:points,anchorError:drag?carton.localToWorld(drag.local.clone()).distanceTo(anchor.position):0,dragging:!!drag,returning:!!returning,progress,scale:carton.scale.x,position:carton.getWorldPosition(new THREE.Vector3()).toArray(),blurredGroups:0,surroundingsVisible:faded.filter(f=>f.o.visible).length,sharpHook:group.children.filter(o=>o!==carton).every(o=>o.layers.mask===2),visible:carton.visible,cartonId:carton.uuid,attached:carton.parent===parent}}};
}

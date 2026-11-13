import * as THREE from '/vendor/three.module.js';
// One renderer, one carton. Reparenting preserves the world transform.
export function createProductView(c){
 const {sceneHost:host,scene,camera,carton,group,render,onSave,onBusy}=c;
 const parent=carton.parent,home=carton.position.clone(),homeQ=carton.quaternion.clone(),savedAngle=c.angle();
 // Full-resolution, premultiplied separable Gaussian. The mask uses the
 // actual scene depth: infrastructure and selected geometry never receive blur.
 const layerMasks=new Map();
 scene.traverse(o=>{layerMasks.set(o,o.layers.mask)});
 for(const other of c.others)other.traverse(o=>o.layers.set(2));
 const lights=[];scene.traverse(o=>{if(o.isLight){lights.push([o,o.layers.mask]);o.layers.enableAll()}});
 const baseBuffer=new THREE.WebGLRenderTarget(1,1),buffer=new THREE.WebGLRenderTarget(1,1),maskBuffer=new THREE.WebGLRenderTarget(1,1),ping=new THREE.WebGLRenderTarget(1,1);
 const composite=new THREE.Scene(),screenCamera=new THREE.OrthographicCamera(-1,1,1,-1,0,1);
 const black=new THREE.MeshBasicMaterial({color:0x000000}),white=new THREE.MeshBasicMaterial({color:0xffffff});
 const blur=new THREE.ShaderMaterial({depthTest:false,depthWrite:false,uniforms:{image:{value:buffer.texture},maskImage:{value:maskBuffer.texture},baseImage:{value:baseBuffer.texture},originalImage:{value:buffer.texture},stepSize:{value:new THREE.Vector2()},finalPass:{value:false}},vertexShader:'varying vec2 uv0;void main(){uv0=uv;gl_Position=vec4(position.xy,0.,1.);}',fragmentShader:`
 uniform sampler2D image;uniform sampler2D maskImage;uniform sampler2D baseImage;uniform sampler2D originalImage;uniform vec2 stepSize;uniform bool finalPass;varying vec2 uv0;
 void main(){vec4 sum=vec4(0.);float weights=0.;
 for(int i=-8;i<=8;i++){vec2 uv=uv0+float(i)*stepSize;float w=exp(-float(i*i)/18.);vec4 sampleColor=texture2D(image,uv);
 if(!finalPass){float coverage=texture2D(maskImage,uv).r;sampleColor=vec4(sampleColor.rgb*coverage,coverage);}
 sum+=sampleColor*w;weights+=w;}
 gl_FragColor=sum/weights;
 if(finalPass){vec4 base=texture2D(baseImage,uv0);gl_FragColor=vec4(gl_FragColor.rgb+base.rgb*(1.-gl_FragColor.a),gl_FragColor.a+base.a*(1.-gl_FragColor.a));
 vec4 mask=texture2D(maskImage,uv0);if(mask.a>.5&&mask.r<.5)gl_FragColor=texture2D(originalImage,uv0);
 // Gaussian coverage is premultiplied in linear light. Unpremultiply
 // before tone/color conversion, then composite in display space; encoding
 // premultiplied RGB directly produces bright fringes on light cartons.
 float coverage=gl_FragColor.a;if(coverage>.00001)gl_FragColor.rgb/=coverage;
 #include <tonemapping_fragment>
 #include <colorspace_fragment>
 gl_FragColor=vec4(gl_FragColor.rgb*coverage+vec3(0.980392,0.980392,0.972549)*(1.-coverage),1.);
 }}`});
 const quad=new THREE.Mesh(new THREE.PlaneGeometry(2,2),blur);composite.add(quad);
 function renderScene(renderer){
  const w=host.clientWidth,h=host.clientHeight,showroom=host.closest('.showroom'),fullW=showroom.clientWidth,fullH=showroom.clientHeight;
  camera.setViewOffset(w,h,0,0,fullW,fullH);const currentSize=renderer.getSize(new THREE.Vector2());if(currentSize.x!==fullW||currentSize.y!==fullH)renderer.setSize(fullW,fullH,false);renderer.domElement.style.width=fullW+'px';renderer.domElement.style.height=fullH+'px';
  const size=renderer.getDrawingBufferSize(new THREE.Vector2());for(const target of [baseBuffer,buffer,maskBuffer,ping])if(target.width!==size.x||target.height!==size.y)target.setSize(size.x,size.y);
  const mask=camera.layers.mask,shadow=renderer.shadowMap.enabled,updateShadows=renderer.shadowMap.autoUpdate;camera.layers.enableAll();
  renderer.setRenderTarget(buffer);renderer.render(scene,camera);renderer.shadowMap.autoUpdate=false;camera.layers.set(0);camera.layers.enable(1);renderer.setRenderTarget(baseBuffer);renderer.render(scene,camera);camera.layers.enableAll();
  renderer.shadowMap.enabled=false;scene.overrideMaterial=black;renderer.setRenderTarget(maskBuffer);renderer.render(scene,camera);
  renderer.autoClear=false;scene.overrideMaterial=white;camera.layers.set(2);renderer.render(scene,camera);renderer.autoClear=true;scene.overrideMaterial=null;renderer.shadowMap.enabled=shadow;
  const radius=renderer.getPixelRatio()*ease(progress)*.8;
  blur.uniforms.image.value=buffer.texture;blur.uniforms.stepSize.value.set(radius/size.x,0);blur.uniforms.finalPass.value=false;renderer.setRenderTarget(ping);renderer.render(composite,screenCamera);
  blur.uniforms.image.value=ping.texture;blur.uniforms.stepSize.value.set(0,radius/size.y);blur.uniforms.finalPass.value=true;renderer.setRenderTarget(null);renderer.clear();
  renderer.setScissorTest(true);renderer.setScissor(0,fullH-h,w,h);renderer.render(composite,screenCamera);renderer.setScissorTest(false);
  // The same detached carton can cross the information card. Draw with depth
  // against the complete scene, but extend the canvas beyond its usual clip.
  if(drag||returning||phase==='disappearing'){renderer.autoClear=false;renderer.clearDepth();camera.layers.set(1);renderer.render(scene,camera);renderer.autoClear=true;}
  camera.layers.mask=mask;renderer.shadowMap.autoUpdate=updateShadows;
 }
 carton.traverse(o=>o.layers.set(1));group.children.filter(o=>o!==carton).forEach(o=>o.traverse(n=>n.layers.set(1)));
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
  if(phase==='zooming'||leaving){progress=Math.max(0,Math.min(1,progress+(leaving?-1:1)*dt/.65));const k=ease(progress);camera.position.lerpVectors(startCamera,focusCamera,k);camera.lookAt(0,.34,3.4);c.setAngle(savedAngle+(c.goal-savedAngle)*k);if(progress===1&&!leaving)setPhase('ready');}
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
 function cleanup(){for(const [o,mask] of layerMasks)o.layers.mask=mask;for(const [o,mask] of lights)o.layers.mask=mask;baseBuffer.dispose();buffer.dispose();maskBuffer.dispose();ping.dispose();black.dispose();white.dispose();blur.dispose();quad.geometry.dispose();carton.quaternion.copy(homeQ);carton.scale.copy(homeScale);carton.visible=true;cancelAnimationFrame(frame);host.removeEventListener('pointerdown',down);host.removeEventListener('pointermove',move);host.removeEventListener('pointerup',up);host.removeEventListener('pointercancel',cancel);host.removeEventListener('lostpointercapture',cancel);scene.remove(anchor);host.classList.remove('dragging','returning','over-target');delete host.dataset.phase;c.cameraLayout(false);c.renderer.setSize(host.clientWidth,host.clientHeight);}
 setPhase('zooming');request();
 return {renderScene,leave(callback){if(leaving)return;leaving=true;last=performance.now();done=callback;if(drag)cancel({pointerId:drag.id});if(!saveAnimation)setPhase('leaving');request()},resize(){c.cameraLayout(false);startCamera.copy(camera.position);c.cameraLayout(true);focusCamera.copy(camera.position);camera.position.lerpVectors(startCamera,focusCamera,ease(progress));if(drag)cancel({pointerId:drag.id});render()},diagnostics(){scene.updateMatrixWorld(true);const bounds=new THREE.Box3().setFromObject(carton),r=c.renderer.domElement.getBoundingClientRect(),points=[];for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){const v=new THREE.Vector3(x,y,z).project(camera);points.push({x:r.left+(v.x+1)*r.width/2,y:r.top+(1-v.y)*r.height/2})}const v=bounds.getCenter(new THREE.Vector3()).project(camera);return {phase,center:{x:r.left+(v.x+1)*r.width/2,y:r.top+(1-v.y)*r.height/2},bounds:points,anchorError:drag?carton.localToWorld(drag.local.clone()).distanceTo(anchor.position):0,dragging:!!drag,returning:!!returning,progress,scale:carton.scale.x,position:carton.getWorldPosition(new THREE.Vector3()).toArray(),blurredGroups:c.others.length,sharpHook:group.children.filter(o=>o!==carton).every(o=>o.layers.mask===2),visible:carton.visible,blurResolution:[buffer.width,buffer.height],cartonId:carton.uuid,attached:carton.parent===parent}}};
}

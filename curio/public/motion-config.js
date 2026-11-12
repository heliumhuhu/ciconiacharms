export const MOTION = Object.freeze({holdMs:250,dragPx:8,wheelQuietMs:140,settleMs:380,dragSensitivity:.006,wheelSensitivity:.0022,previewTolerance:.025,swingStiffness:48,swingDamping:7,swingImpulse:2.8,maxSwing:.14});
export const wrap = a => Math.atan2(Math.sin(a),Math.cos(a));
export function sectorAngles(products){return products.map(p=>{const group=products.filter(x=>x.category===p.category);return (p.category==='toys'?Math.PI:0)+(group.indexOf(p)-(group.length-1)/2)*Math.PI/group.length;});}
export function closestIndex(angles,angle){return angles.reduce((best,a,i)=>Math.abs(wrap(a+angle))<Math.abs(wrap(angles[best]+angle))?i:best,0);}

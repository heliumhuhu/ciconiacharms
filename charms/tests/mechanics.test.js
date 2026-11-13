import test from 'node:test';
import assert from 'node:assert/strict';
import {sectorAngles,closestIndex,wrap} from '../public/motion-config.js';
import {readBag,changeQuantity,totalQuantity} from '../public/bag.js';
test('unequal categories retain opposite half sectors and actual snap positions',()=>{const p=[...Array(3)].map((_,i)=>({id:i,category:'jewellery'})).concat([...Array(8)].map((_,i)=>({id:3+i,category:'toys'})));const a=sectorAngles(p);a.forEach((v,i)=>{assert.ok(Math.abs(wrap(v-(i<3?0:Math.PI)))<Math.PI/2);assert.equal(closestIndex(a,-v),i)});assert.equal(new Set(a).size,11)});
test('quantities increase, decrement and preserve unknown IDs',()=>{let b={'deleted-product':2};b=changeQuantity(b,'p1',1);b=changeQuantity(b,'p1',1);assert.equal(totalQuantity(b),4);b=changeQuantity(b,'p1',-1);assert.equal(b.p1,1);assert.equal(b['deleted-product'],2);assert.equal(changeQuantity(b,'p1',-1).p1,undefined)});
test('corrupt and inaccessible storage are safe',()=>{assert.deepEqual(readBag({getItem(){throw Error()}}),{});assert.deepEqual(readBag({getItem:()=>'{bad'}),{});assert.deepEqual(readBag({getItem:()=>'{"p":2,"negative":-1,"float":1.4,"huge":10000}'}),{p:2})});
test('old distinct saved IDs migrate to one unit each',()=>{assert.deepEqual(readBag({getItem:key=>key==='curio-box'?'[1,2,2]':null}),{'product-1':1,'product-2':1})});

test('Charms migrates legacy quantities and current storage takes precedence',()=>{const old={'product-1':3};assert.deepEqual(readBag({getItem:key=>key==='curio-quantities'?JSON.stringify(old):null}),old);assert.deepEqual(readBag({getItem:key=>key==='ciconia-charms-quantities'?'{}':JSON.stringify(old)}),{});});

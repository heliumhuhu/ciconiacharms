import {rmSync,mkdirSync,cpSync} from 'node:fs';
rmSync('dist',{recursive:true,force:true});mkdirSync('dist');
cpSync('public','dist/public',{recursive:true});cpSync('server.js','dist/server.js');
console.log('Production server and local assets built in dist/');

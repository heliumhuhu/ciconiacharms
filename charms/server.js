import express from 'express';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('./public/',import.meta.url));
const app=express();app.disable('x-powered-by');
app.get(['/','/jewellery','/toys'],(_,res)=>res.sendFile(root+'index.html'));
app.use(express.static(root,{index:false}));
app.listen(Number(process.env.PORT||3000),process.env.HOST||'0.0.0.0',()=>console.log('CICONIA CHARMS listening'));

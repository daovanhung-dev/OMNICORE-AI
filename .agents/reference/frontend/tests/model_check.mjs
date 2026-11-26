import assert from 'node:assert/strict';
import test from 'node:test';
import {decodePage} from '../dist/app/features/shared/SH01/models/item.model.js';
import {getJson,HttpError} from '../dist/app/core/http/api-client.js';
import {getAccessToken,setAccessToken,clearSession} from '../dist/app/core/auth/session.js';
const valid={data:{items:[{id:1,name:'Mục'}],total:1,page:1,page_size:1}};
test('valid-page',()=>assert.deepEqual(decodePage(valid),valid.data));
const invalid=[null,{}, {data:null},{data:{...valid.data,items:[{id:'1',name:'Mục'}]}},{data:{...valid.data,total:-1}},{data:{...valid.data,page:0}},{data:{...valid.data,page_size:0}}];
invalid.forEach((value,i)=>test('invalid-page-'+i,()=>assert.throws(()=>decodePage(value))));
test('http-auth-and-401',async()=>{
  const original=globalThis.fetch;setAccessToken('test-token');
  try {globalThis.fetch=async(path,options)=>{assert.equal(options.headers.Authorization,'Bearer test-token');return new Response('{}',{status:401,headers:{'X-Request-ID':'trace'}})};
  await assert.rejects(getJson('/api/v1/items',new AbortController().signal),e=>e instanceof HttpError&&e.status===401&&e.traceId==='trace');assert.equal(getAccessToken(),undefined);
  } finally {globalThis.fetch=original;clearSession();}
});
test('http-external-path',async()=>assert.rejects(getJson('https://example.com',new AbortController().signal)));
test('http-timeout',async()=>{
 const original=globalThis.fetch;try{globalThis.fetch=async(path,opt)=>new Promise((_,reject)=>opt.signal.addEventListener('abort',()=>reject(new Error('timeout'))));await assert.rejects(getJson('/api/v1/items',new AbortController().signal,1));}finally{globalThis.fetch=original;}
});

const path=require('path'), fs=require('fs');
const src=fs.readFileSync(path.join(__dirname,'../../variantes/flaques.js'),'utf8');
const W={}; (new Function('window','performance', src)).call(W, W, {now:()=>0}); const F=W.Flaques;
const l=390,h=844,PAS=4,NX=Math.ceil(l/PAS)+1,NY=Math.ceil(h/PAS)+1;
const US=[0.08,0.2,0.35,0.5,0.65,0.8,0.93]; const tot={}; const msT=[];
for(let s=1;s<=8;s++){ const G=F.germesCouverture(l,h,F.alea(s*7919+3)); const A=new Float32Array(NX*NY);
  for(const u of US){ const t0=process.hrtime.bigint(); F.champ(A,NX,NY,0,0,PAS,G,F.avance(u),u*3.2); msT.push(Number(process.hrtime.bigint()-t0)/1e6); let n=0; for(let i=0;i<A.length;i++) if(A[i]>0) n++; (tot[u]=tot[u]||[]).push(Math.round(100*n/A.length)); } }
for(const u of US) console.log(u, tot[u].join(' '));
msT.sort((a,b)=>a-b); console.log('ms champ médiane', msT[msT.length>>1].toFixed(1), 'max', msT[msT.length-1].toFixed(1));

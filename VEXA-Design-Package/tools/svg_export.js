() => {
  const W=innerWidth,H=document.documentElement.scrollHeight;
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let n=0;
  const defs=[],parts=[];
  const canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');
  const num=v=>Math.round(v*100)/100;
  const paint=c=>c&&c!=='transparent'&&c!=='rgba(0, 0, 0, 0)';
  const box=el=>{const r=el.getBoundingClientRect();return {x:r.left+scrollX,y:r.top+scrollY,w:r.width,h:r.height};};
  const rect=(r,fill,extra='')=>`<rect x="${num(r.x)}" y="${num(r.y)}" width="${num(r.w)}" height="${num(r.h)}" fill="${esc(fill)}" ${extra}/>`;
  const font=(c)=>{try{ctx.font=`${c.fontStyle} ${c.fontWeight} ${c.fontSize} ${c.fontFamily}`;}catch{}const m=ctx.measureText('Ag');return {a:m.fontBoundingBoxAscent||parseFloat(c.fontSize)*.9,d:m.fontBoundingBoxDescent||parseFloat(c.fontSize)*.2};};
  function textNode(node,c){
    if(!node.textContent.trim())return '';
    const value=node.textContent,rg=document.createRange();let out='';
    const metrics=font(c);
    for(const m of value.matchAll(/\S+\s*/g)){
      rg.setStart(node,m.index);rg.setEnd(node,m.index+m[0].length);
      const rr=rg.getBoundingClientRect();if(!rr.width||!rr.height)continue;
      let t=m[0];if(c.textTransform==='uppercase')t=t.toUpperCase();if(c.textTransform==='lowercase')t=t.toLowerCase();
      const baseline=rr.top+scrollY+(rr.height-metrics.a-metrics.d)/2+metrics.a;
      out+=`<text x="${num(rr.left+scrollX)}" y="${num(baseline)}" fill="${esc(c.color)}" font-family="${esc(c.fontFamily)}" font-size="${esc(c.fontSize)}" font-weight="${esc(c.fontWeight)}" font-style="${esc(c.fontStyle)}" letter-spacing="${c.letterSpacing==='normal'?0:esc(c.letterSpacing)}" xml:space="preserve">${esc(t)}</text>`;
    }
    return out;
  }
  function after(el,r){
    const c=getComputedStyle(el,'::after');
    if(c.content==='none'||c.display==='none')return '';
    if(el.classList.contains('hero-photo')){
      const id='gradient-'+(++n),mobile=innerWidth<=760;
      defs.push(`<linearGradient id="${id}" x1="0" y1="${mobile?'1':'0'}" x2="${mobile?'0':'1'}" y2="0"><stop offset="0" stop-color="#171715"/><stop offset="${mobile?'.6':'.2'}" stop-color="#171715" stop-opacity="0"/><stop offset="1" stop-color="#171715" stop-opacity=".1"/></linearGradient>`);
      return rect(r,`url(#${id})`);
    }
    if(el.tagName==='SUMMARY')return `<text x="${r.x+r.w-10}" y="${r.y+r.h/2+5}" fill="${c.color}" font-family="Arial" font-size="16">${el.parentElement.open?'−':'+'}</text>`;
    return '';
  }
  function draw(el){
    if(el.nodeType!==1)return '';
    const c=getComputedStyle(el),r=box(el);
    if(c.display==='none'||c.visibility==='hidden'||c.opacity==='0'||!r.w||!r.h||el.classList.contains('sr-only')||el.classList.contains('skip-link')||['SCRIPT','STYLE','LINK','META','NOSCRIPT','DIALOG','OPTION'].includes(el.tagName))return '';
    let body='';const radius=c.borderRadius.includes('%')?Math.min(r.w,r.h)*parseFloat(c.borderRadius)/100:parseFloat(c.borderRadius)||0;
    if(paint(c.backgroundColor))body+=rect(r,c.backgroundColor,radius?`rx="${num(radius)}"`:'');
    if(c.backgroundImage.includes('linear-gradient')&&el.classList.contains('hero-copy')){
      const id='gradient-'+(++n);defs.push(`<linearGradient id="${id}"><stop offset="0" stop-color="#171715" stop-opacity=".84"/><stop offset="1" stop-color="#171715" stop-opacity=".05"/></linearGradient>`);body+=rect(r,`url(#${id})`);
    }
    const roundedBorder=radius>0&&parseFloat(c.borderTopWidth)>0&&c.borderTopWidth===c.borderBottomWidth&&c.borderLeftWidth===c.borderRightWidth;
    if(roundedBorder)body+=rect(r,'none',`rx="${num(radius)}" stroke="${c.borderTopColor}" stroke-width="${c.borderTopWidth}"`);
    if(el.classList.contains('size-button')&&el.disabled)body+=`<line x1="${r.x}" y1="${r.y+r.h}" x2="${r.x+r.w}" y2="${r.y}" stroke="#c3beb4" stroke-width="1"/>`;
    if(!roundedBorder) for(const [side,x1,y1,x2,y2] of [['Top',r.x,r.y,r.x+r.w,r.y],['Bottom',r.x,r.y+r.h,r.x+r.w,r.y+r.h],['Left',r.x,r.y,r.x,r.y+r.h],['Right',r.x+r.w,r.y,r.x+r.w,r.y+r.h]]){
      const bw=parseFloat(c['border'+side+'Width']);if(bw&&c['border'+side+'Style']!=='none'&&paint(c['border'+side+'Color']))body+=`<line x1="${num(x1)}" y1="${num(y1)}" x2="${num(x2)}" y2="${num(y2)}" stroke="${c['border'+side+'Color']}" stroke-width="${bw}"/>`;
    }
    if(el.tagName==='IMG'){
      const naturalW=el.naturalWidth,naturalH=el.naturalHeight;
      const ar=c.objectFit==='contain'?'xMidYMid meet':'xMidYMid slice';
      body+=`<svg x="${num(r.x)}" y="${num(r.y)}" width="${num(r.w)}" height="${num(r.h)}" viewBox="0 0 ${num(r.w)} ${num(r.h)}" overflow="hidden"><image width="${num(r.w)}" height="${num(r.h)}" href="${esc(el.src)}" preserveAspectRatio="${ar}" style="mix-blend-mode:${c.mixBlendMode}"/></svg>`;
    }else if(el.tagName.toLowerCase()==='svg'){
      const clone=el.cloneNode(true);clone.setAttribute('x',num(r.x));clone.setAttribute('y',num(r.y));clone.setAttribute('width',num(r.w));clone.setAttribute('height',num(r.h));clone.setAttribute('color',c.color);body+=clone.outerHTML;
    }else if(el.tagName==='INPUT'||el.tagName==='SELECT'){
      if(['radio','checkbox'].includes(el.type)){
        if(el.type==='radio')body+=`<circle cx="${r.x+r.w/2}" cy="${r.y+r.h/2}" r="${r.w/2-1}" fill="none" stroke="#6b675f"/>${el.checked?`<circle cx="${r.x+r.w/2}" cy="${r.y+r.h/2}" r="${r.w/4}" fill="#171715"/>`:''}`;
        else body+=rect(r,el.checked?'#171715':'none','stroke="#6b675f"')+(el.checked?`<path d="M${r.x+3} ${r.y+r.h/2}l3 3 7-7" stroke="white" fill="none"/>`:'');
      }else{
        const t=el.tagName==='SELECT'?el.options[el.selectedIndex]?.text:el.value||el.placeholder;
        const metrics=font(c);body+=`<text x="${num(r.x+parseFloat(c.paddingLeft)+parseFloat(c.borderLeftWidth))}" y="${num(r.y+r.h/2+(metrics.a-metrics.d)/2)}" font-family="${esc(c.fontFamily)}" font-size="${c.fontSize}" fill="${el.value?c.color:'#777268'}">${esc(t)}</text>`;
      }
    }else{
      const nodes=[...el.childNodes];
      const sorted=nodes.map((node,i)=>({node,i,z:node.nodeType===1?parseInt(getComputedStyle(node).zIndex)||0:0})).sort((a,b)=>a.z-b.z||a.i-b.i);
      for(const {node} of sorted){
        if(node.nodeType===3)body+=textNode(node,c);
        else if(node.nodeType===1){body+=draw(node);if(el.classList.contains('hero-photo')&&node.tagName==='IMG')body+=after(el,r);}
      }
      if(!el.classList.contains('hero-photo'))body+=after(el,r);
    }
    let clip='';
    if(['hidden','clip'].includes(c.overflow)&&!['IMG','svg'].includes(el.tagName)){
      const id='clip-'+(++n);defs.push(`<clipPath id="${id}">${rect(r,'#fff',radius?`rx="${num(radius)}"`:'')}</clipPath>`);clip=` clip-path="url(#${id})"`;
    }
    const opacity=c.opacity!=='1'?` opacity="${c.opacity}"`:'';
    const label=el.id||el.classList[0]||el.tagName.toLowerCase();
    return `<g id="layer-${++n}" data-name="${esc(label)}"${clip}${opacity}>${body}</g>`;
  }
  const content=draw(document.body);
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><title>${esc(document.title)} / editable screen snapshot</title><desc>Editable text and shape snapshot. Photography remains raster. Canonical responsive behaviour is in HTML and CSS; this is not a native Figma Auto Layout document.</desc><defs>${defs.join('')}</defs>${content}</svg>`;
}

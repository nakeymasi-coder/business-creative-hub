(function(){
  'use strict';

  const byId=(id)=>document.getElementById(id);
  const cleanText=(s='')=>String(s)
    .replace(/^#{1,6}\s+/gm,'')
    .replace(/\*\*(.*?)\*\*/g,'$1')
    .replace(/__(.*?)__/g,'$1')
    .trim();

  function state(){ return window.GLAM_GET_MERGED ? window.GLAM_GET_MERGED() : null; }
  function save(next){ if(window.GLAM_SET_MERGED) window.GLAM_SET_MERGED(next); }
  function toastMsg(msg){ if(typeof window.toast==='function') window.toast(msg); }

  function brandContext(){
    const parts=[];
    const add=(label,id)=>{ const v=(byId(id)?.value||'').trim(); if(v) parts.push(`${label}: ${v}`); };
    add('Brand','brandName');
    add('Brand voice','brandVoice');
    add('Primary audience','brandAudience');
    add('Visual style','brandStyle');
    add('Website','brandWebsite');
    add('Store','brandStore');
    return parts.join('\n').slice(0,3000);
  }

  function addIdeaMessage(role,body){
    const s=state();
    if(!s) return;
    s.ideas = Array.isArray(s.ideas) ? s.ideas : [];
    s.ideas.push({
      id:(crypto.randomUUID?crypto.randomUUID():'idea_'+Date.now()+Math.random().toString(36).slice(2)),
      role,
      body,
      created:new Date().toISOString()
    });
    save(s);
  }

  async function developIdea(){
    const input=byId('mergedIdeaInput');
    const btn=byId('mergedDevelopIdea');
    const idea=(input?.value||'').trim();
    if(!idea){ toastMsg('Enter an idea first.'); return; }

    const before=state();
    const history=(before?.ideas||[]).slice(-8).map(m=>({role:m.role,body:m.body}));

    addIdeaMessage('user',idea);
    if(input) input.value='';

    const oldLabel=btn?.textContent||'Develop Idea';
    if(btn){ btn.disabled=true; btn.textContent='Thinking for you...'; }

    try{
      const client=window.GLAM_SUPABASE_CLIENT;
      if(!client) throw new Error('The private AI connection is not ready. Refresh the hub and try again.');

      const {data,error}=await client.functions.invoke('idea-brain',{
        body:{ idea, history, brandContext:brandContext() }
      });
      if(error) throw error;
      if(data?.error) throw new Error(data.error);
      const answer=cleanText(data?.text||'');
      if(!answer) throw new Error('Idea Brain returned an empty response.');

      addIdeaMessage('assistant',answer);
      toastMsg('Idea Brain developed the concept for you.');
    }catch(err){
      console.error('Idea Brain AI error',err);
      const message=String(err?.message||err||'Idea Brain could not connect to AI.');
      addIdeaMessage('assistant',`I could not finish the AI analysis yet. ${message}`);
      toastMsg('Idea Brain could not finish the AI analysis.');
    }finally{
      if(btn){ btn.disabled=false; btn.textContent=oldLabel; }
    }
  }

  function bind(){
    const btn=byId('mergedDevelopIdea');
    if(btn){
      btn.onclick=developIdea;
      btn.dataset.aiIdeaBrain='1';
    }
    if(!document.getElementById('ideaBrainAiStyle')){
      const style=document.createElement('style');
      style.id='ideaBrainAiStyle';
      style.textContent='.idea-msg.assistant,.idea-msg.user{white-space:pre-wrap}.idea-msg.assistant{max-width:94%}.idea-msg assistant{}';
      document.head.appendChild(style);
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',bind,{once:true});
  else bind();
  setTimeout(bind,500);
})();

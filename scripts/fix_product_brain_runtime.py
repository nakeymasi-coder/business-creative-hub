from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- PRODUCT_BRAIN_RUNTIME_FIX -->'
if marker in s:
    print('Product Brain runtime fix already present')
    raise SystemExit(0)

# Remove the broken Product Brain block that was written as literal \\n text.
start=s.find('\\n<script>\\n(function(){\\n  const byId=')
if start!=-1:
    end=s.find('\\n</script>\\n', start)
    if end!=-1:
        s=s[:start]+s[end+len('\\n</script>\\n'):]

script=r'''
<!-- PRODUCT_BRAIN_RUNTIME_FIX -->
<script>
(function(){
  const byId=id=>document.getElementById(id);
  const val=id=>(byId(id)?.value||'').trim();
  const put=(id,v,onlyBlank=false)=>{const e=byId(id);if(e&&(!onlyBlank||!String(e.value||'').trim()))e.value=v;};
  const defs={
    'Prompt Pack':['prompt pack','PDF prompt pack / digital prompt collection','Instant digital download','Commercial creation use','$17','$27','$12','Get the prompts','Ready-to-use prompts, quick-start instructions, customization guidance, and examples'],
    'Digital Guide / Ebook':['digital guide','PDF guide / ebook','Instant PDF download','Personal use','$27','$37','$17','Get the guide','Step-by-step guidance, examples, action steps, and quick-reference tips'],
    'Workshop / Class':['workshop','Live or recorded online workshop','Online class access','Personal learning use','$97','$147','$77','Reserve your spot','Guided training, demonstrations, practical examples, action steps, and supporting resources'],
    'Generator / Tool':['generator','Interactive generator / web app','Online tool access','Commercial creation use','$27','$47','$17','Get access','Interactive generator, guided options, reusable outputs, and beginner-friendly instructions'],
    'Template Pack':['template pack','Editable digital template pack','Instant digital download','Commercial creation use','$27','$47','$17','Get the templates','Editable templates, usage instructions, and customization guidance'],
    'Printable':['printable','Printable PDF','Instant PDF download','Personal use','$9','$17','$7','Get the printable','Print-ready pages, instructions, and reusable worksheets'],
    'Membership / Community':['membership','Online membership / community','Private community access','Member use','$47/month','$67/month','$37/month','Join now','Community access, ongoing resources, support, updates, and member content'],
    'Bundle':['digital bundle','Digital resource bundle','Instant digital download / access','Commercial creation use','$47','$67','$37','Get the bundle','Multiple coordinated resources, guides, templates, prompts, or tools in one bundle'],
    'Other Digital Product':['digital product','Digital product','Instant digital delivery','Personal or commercial use as stated','$27','$37','$17','Get instant access','Core digital resource, instructions, and supporting materials']
  };
  function goal(t,c){t=t.toLowerCase();if(/image|graphic|visual|photo|art|design|thumbnail/.test(t))return'create polished visual content faster';if(/video|reel|tiktok|youtube|short.form/.test(t))return'create video content faster and with clearer direction';if(/market|promotion|social|content|caption|launch|sell|sales/.test(t))return'market and sell their offers with less guesswork';if(/website|site|landing|page/.test(t))return'build and improve their online presence more easily';if(/prompt|generator|ai/.test(t))return'turn ideas into usable AI-ready outputs faster';if(/organize|planner|checklist|workflow|system/.test(t))return'get organized with a repeatable system';if(/learn|teach|class|workshop|guide|tutorial/.test(t))return'learn the process step by step and put it into action';if(c==='Membership / Community')return'get ongoing support, resources, and momentum';return'get a useful result faster with a clearer, simpler process';}
  function audience(t,c){t=t.toLowerCase();if(/teacher|educator/.test(t))return'teachers and educators who want a simpler way to create and use digital resources';if(/coach|coaching/.test(t))return'coaches and service providers who want practical, ready-to-use business resources';if(/creator|content|social/.test(t))return'digital creators and small business owners who want to create and market content faster';if(/beginner|easy|simple|step.by.step/.test(t))return'beginners who want clear guidance without technical overwhelm';if(c==='Workshop / Class')return'beginners and growing business owners who want guided, hands-on help';return window.data?.brand?.audience||'beginners, creators, and small business owners who want practical help without unnecessary overwhelm';}
  function build(){
    const name=val('productName'),cat=val('productCategory')||'Other Digital Product',desc=val('productPlainDescription'),inc=val('productPlainIncludes');
    if(!name){toast?.('Add the product name first.');byId('productName')?.focus();return;}
    if(!desc){toast?.('Tell the hub what the product is in your own words.');byId('productPlainDescription')?.focus();return;}
    const d=defs[cat]||defs['Other Digital Product'],g=goal(name+' '+desc+' '+inc,cat),a=audience(name+' '+desc+' '+inc,cat),clean=desc.replace(/\s+/g,' ').replace(/[.]$/,'');
    put('productInternalName',name,true);put('productFormat',d[1]);put('productPrice',d[4],true);put('productRegularPrice',d[5],true);put('productSalePrice',d[6],true);
    put('productSummary',`${name} is a ${d[0]} that ${clean.charAt(0).toLowerCase()+clean.slice(1)}. It is designed to help ${a} ${g}.`);
    put('productProblem','The customer wants the result, but the process can feel confusing, time-consuming, or hard to organize. They may not know what to create, what steps matter most, or how to turn an idea into a finished result.');
    put('productTransformation',`Go from unsure, scattered, or starting from scratch to having a clear resource that helps them ${g}.`);
    put('productPrimaryBenefit',g.replace(/\b\w/g,m=>m.toUpperCase()));put('productSecondaryBenefits','Saves time, reduces guesswork, gives clear direction, creates a repeatable process, and makes the next step easier');
    put('productIncludes',inc||d[8]);put('productBonuses','Suggested bonus: quick-start guide, example output, and a simple what-to-do-next checklist');put('productRights',d[3]);put('productDelivery',d[2]);
    put('productAudience',a);put('productSkill','Beginner-friendly / no advanced experience required');put('productPainPoints','Not knowing where to start; spending too much time figuring things out; feeling overwhelmed by too many steps; inconsistent results; needing a clearer shortcut or repeatable process');
    put('productDesiredResult',`${g.replace(/\b\w/g,m=>m.toUpperCase())} with more confidence, less guesswork, and a practical process they can use again.`);put('productBuyReasons','It gives them a faster starting point; simplifies a confusing process; saves time; feels practical instead of overwhelming; provides reusable value; helps them move from idea to action.');
    put('productHesitations','They may wonder whether it is easy enough for them, whether they need special tools or experience, what exactly is included, and whether the product will save them enough time to be worth buying.');put('productCTA',d[7]);put('productPrimaryAngle',`${g.replace(/\b\w/g,m=>m.toUpperCase())} — without starting from scratch`);put('productSecondaryAngles','Save time and skip the guesswork; beginner-friendly guidance; turn an idea into action faster; reusable value; clear next steps instead of overwhelm');
    put('productKeywords',[name,cat,'beginner friendly',g,'digital product','easy to use','time saving'].join(', '));put('productSEO',`${name}; ${cat}; ${g}; beginner-friendly ${d[0]}; digital resource for ${a}`);
    const r=byId('productBrainResult');if(r){r.classList.add('product-brain-done');r.innerHTML=`<b>Done.</b> The hub built the strategy for <b>${name}</b>. You can save it now, or review Hub-Generated Product Intelligence if you want.`;}
    toast?.('Product Brain finished the strategy for you.');
  }
  window.buildProductBrain=build;
  const bind=()=>{const b=byId('easyFillProductBtn');if(b){b.onclick=e=>{e.preventDefault();build();};}};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});else bind();
})();
</script>
'''

s=s.replace('</body>',script+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Product Brain runtime fix injected')

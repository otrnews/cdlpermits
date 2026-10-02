// ===== Settings: where the results screen sends people =====
var LINKS = {
  course: 'https://www.mycdlcoach.com/theory-and-endorsements',  // ELDT theory course ($149)
  lounge: 'https://www.mycdlcoach.com/offers/DzKSWbj5/checkout'  // Free Driver's Lounge sign-up
};
var ES = document.documentElement.lang === 'es';
var S = ES ? {
  how:'¿Cómo quiere practicar?', best:'Su mejor puntaje: ', practice:'Modo práctica', practiceD:'Vea la respuesta correcta y por qué después de cada pregunta.',
  exam:'Modo examen', examD:'Sin pistas hasta el final, como el examen real.', fix:'Corregir mis errores', fixD:'Repita solo las preguntas que falló antes.',
  fixing:'Corrigiendo errores', read:'🔊 Leer en voz alta', q:'Pregunta ', of:' de ', soFar:' correctas', ok:'¡Correcto!', no:'No exactamente.',
  score:'Ver mi puntaje', next:'Siguiente pregunta', passed:function(n){return '¡Aprobó '+n+'!';}, fixed:'¡Errores corregidos!', notYet:'Todavía no aprueba.',
  got:function(r,t){return 'Acertó '+r+' de '+t+'. La mayoría de los estados piden 80% para aprobar.';}, streak:'días seguidos estudiando',
  passH:'Su siguiente paso: la teoría ELDT', passP:'Antes del examen práctico de la CDL, la ley federal exige la capacitación ELDT (teoría) con un proveedor registrado. El curso de MyCDLCoach es certificado por la FMCSA, 100% en línea, y la mayoría lo termina en menos de un día.',
  passB:'Obtener mi certificado ELDT, $149', notReady:'¿No está listo para pagar? ', lounge:'Únase gratis al Driver\'s Lounge',
  failH:'Reciba ayuda para llegar al 80%', failP:'Únase gratis al Driver\'s Lounge de MyCDLCoach. Pregunte a conductores con experiencia sobre lo que le costó trabajo y conecte con otros que están sacando su CDL.',
  again:'Repetir el examen', share:'Compartir mi puntaje', other:'Elegir otro examen', review:'Repase lo que falló', yours:'Su respuesta: ',
  shareT:function(p,n){return 'Saqué '+p+'% en el examen de práctica CDL de '+n+'. ¿Puede superarlo?';}, copied:'Enlace copiado. Péguelo donde quiera.', voice:'es-US', home:'/examen-cdl-en-espanol'
} : {
  how:'How do you want to practice?', best:'Your best score: ', practice:'Practice mode', practiceD:'See the right answer and why after every question.',
  exam:'Exam mode', examD:'No hints until the end, just like the real test.', fix:'Fix my mistakes', fixD:'Retake only the questions you got wrong before.',
  fixing:'Fixing mistakes', read:'🔊 Read aloud', q:'Question ', of:' of ', soFar:' correct so far', ok:'Correct.', no:'Not quite.',
  score:'See my score', next:'Next question', passed:function(n){return 'You passed '+n+'!';}, fixed:'Mistakes fixed!', notYet:'Not passing yet.',
  got:function(r,t){return 'You got '+r+' of '+t+' right. Most states require 80% to pass.';}, streak:'-day study streak',
  passH:'Your next step: ELDT theory', passP:'Before your CDL skills test, federal rules require Entry-Level Driver Training theory from a registered provider. MyCDLCoach\'s course is FMCSA-certified, 100% online, and most students finish in under a day. Your certificate is uploaded to the FMCSA the same day.',
  passB:'Get my ELDT certificate, $149', notReady:'Not ready to pay? ', lounge:'Join the free Driver\'s Lounge',
  failH:'Get help reaching 80%', failP:'Join the free MyCDLCoach Driver\'s Lounge. Ask working drivers about the questions that tripped you up, get study tips, and connect with people going through the same process.',
  again:'Take it again', share:'Share my score', other:'Pick another test', review:'Review what you missed', yours:'Your answer: ',
  shareT:function(p,n){return 'I scored '+p+'% on the CDL '+n+' practice test. Can you beat it?';}, copied:'Link copied. Paste it anywhere to share.', voice:'en-US', home:'/'
};
var PASS = 80;
// ===========================================================

function track(url, tag){return url+(url.indexOf('?')>-1?'&':'?')+'utm_source=cdlpermits&utm_medium=results&utm_campaign='+tag;}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function shuffle(a){a=a.slice();for(var k=a.length-1;k>0;k--){var j=Math.floor(Math.random()*(k+1));var t=a[k];a[k]=a[j];a[j]=t;}return a;}
function today(){var d=new Date();return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();}

// ----- Saved progress (stays on this device) -----
var Store={
  get:function(){try{return JSON.parse(localStorage.getItem('cdlpermits')||'{}');}catch(e){return {};}},
  set:function(s){try{localStorage.setItem('cdlpermits',JSON.stringify(s));}catch(e){}},
  best:function(slug){return (this.get().best||{})[slug];},
  saveBest:function(slug,p){var s=this.get();s.best=s.best||{};if(!(s.best[slug]>=p))s.best[slug]=p;this.set(s);},
  missed:function(slug){return (this.get().missed||{})[slug]||[];},
  setMissed:function(slug,arr){var s=this.get();s.missed=s.missed||{};s.missed[slug]=arr;this.set(s);},
  studied:function(){var s=this.get(),t=today();var st=s.streak||{n:0,last:null};
    if(st.last!==t){var y=new Date();y.setDate(y.getDate()-1);
      var ys=y.getFullYear()+'-'+(y.getMonth()+1)+'-'+y.getDate();
      st.n=(st.last===ys)?st.n+1:1;st.last=t;s.streak=st;this.set(s);}return st.n;},
  streak:function(){var st=(this.get().streak)||{};if(!st.last)return 0;
    var y=new Date();y.setDate(y.getDate()-1);var ys=y.getFullYear()+'-'+(y.getMonth()+1)+'-'+y.getDate();
    return (st.last===today()||st.last===ys)?st.n:0;}
};

// ----- Read aloud (free, built into phones) -----
function speak(text){try{speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang=S.voice;u.rate=.95;speechSynthesis.speak(u);}catch(e){}}
var canSpeak='speechSynthesis' in window;

// ----- Confetti for passing -----
function confetti(){
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var c=document.getElementById('confetti');if(!c)return;var x=c.getContext('2d');
  c.width=innerWidth;c.height=innerHeight;c.style.display='block';
  var cols=['#0F5FF8','#F3C300','#FFFFFF','#2980B9','#0A7A45'],ps=[];
  for(var i=0;i<140;i++)ps.push({x:Math.random()*c.width,y:-20-Math.random()*c.height*.5,w:6+Math.random()*6,h:10+Math.random()*8,
    vy:2+Math.random()*3,vx:-1.5+Math.random()*3,r:Math.random()*6,vr:-.2+Math.random()*.4,c:cols[i%cols.length]});
  var t0=Date.now();
  (function f(){x.clearRect(0,0,c.width,c.height);ps.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.r+=p.vr;
    x.save();x.translate(p.x,p.y);x.rotate(p.r);x.fillStyle=p.c;x.fillRect(-p.w/2,-p.h/2,p.w,p.h);x.restore();});
    if(Date.now()-t0<3500)requestAnimationFrame(f);else{x.clearRect(0,0,c.width,c.height);c.style.display='none';}})();
}

// ----- Share -----
function share(text){
  var url='https://cdlpermits.com'+location.pathname;
  if(navigator.share){navigator.share({title:'CDL Permits',text:text,url:url}).catch(function(){});return;}
  try{navigator.clipboard.writeText(text+' '+url);alert(S.copied);}catch(e){prompt('Copy this link:',url);}
}

// ===== Test page =====
(function(){
  var data=window.QUIZ;if(!data)return;
  var box=document.getElementById('quiz');
  var qs,i,right,missed,mode,answers;

  function menu(){
    var m=Store.missed(data.slug),b=Store.best(data.slug);
    var h='<h2 class="menu-h">'+S.how+'</h2>'+
      (b!=null?'<p class="count">'+S.best+b+'%</p>':'')+
      '<div class="modes">'+
      '<button class="mode" type="button" data-m="practice"><strong>'+S.practice+'</strong><span>'+S.practiceD+'</span></button>'+
      '<button class="mode" type="button" data-m="exam"><strong>'+S.exam+'</strong><span>'+S.examD+'</span></button>';
    if(m.length)h+='<button class="mode mode-warn" type="button" data-m="missed"><strong>'+S.fix+' ('+m.length+')</strong><span>'+S.fixD+'</span></button>';
    h+='</div>';
    box.innerHTML=h;
    box.querySelectorAll('.mode').forEach(function(b){b.addEventListener('click',function(){start(b.getAttribute('data-m'));});});
  }

  function start(m){
    mode=m;
    var pool=data.questions;
    if(m==='missed'){var set=Store.missed(data.slug);pool=pool.filter(function(q){return set.indexOf(q.q)>-1;});}
    qs=shuffle(pool);if(data.limit&&m!=='missed')qs=qs.slice(0,data.limit);i=0;right=0;missed=[];answers=[];show();
    box.scrollIntoView({behavior:'smooth',block:'start'});
  }

  function show(){
    var q=qs[i],opts=shuffle([q.a].concat(q.w)),pct=Math.round(i/qs.length*100);
    var label=mode==='exam'?S.exam:(mode==='missed'?S.fixing:S.practice);
    var h='<div class="qbar"><span class="pill">'+label+'</span>'+
      (canSpeak?'<button class="say" type="button" id="say" aria-label="Read the question aloud">'+S.read+'</button>':'')+'</div>'+
      '<div class="lane" aria-hidden="true"><span style="width:'+pct+'%"></span></div>'+
      '<p class="count">'+S.q+(i+1)+S.of+qs.length+(mode!=='exam'?', '+right+S.soFar:'')+'</p>'+
      '<h2 id="qtext">'+esc(q.q)+'</h2><div class="opts" role="group" aria-labelledby="qtext">';
    opts.forEach(function(o,k){h+='<button class="opt" type="button"><span class="key">'+'ABCD'[k]+'</span>'+esc(o)+'</button>';});
    h+='</div><div id="after" aria-live="polite"></div>';
    box.innerHTML=h;
    var btns=box.querySelectorAll('.opt');
    btns.forEach(function(b,k){b.addEventListener('click',function(){answer(b,btns,q,opts[k]);});});
    var s=document.getElementById('say');
    if(s)s.addEventListener('click',function(){speak(q.q+'. '+opts.map(function(o,k){return 'ABCD'[k]+'. '+o;}).join('. '));});
  }

  function answer(b,btns,q,choice){
    var ok=choice===q.a,last=i===qs.length-1;
    btns.forEach(function(x){x.disabled=true;});
    if(ok)right++;else missed.push(q);
    answers.push({q:q,choice:choice,ok:ok});
    if(mode==='exam'){b.classList.add('picked');setTimeout(function(){if(last)done();else{i++;show();}},250);return;}
    btns.forEach(function(x){if(x.textContent.slice(1)===q.a){x.classList.add('right');x.insertAdjacentHTML('beforeend','<span class="mark">✓</span>');}});
    if(!ok){b.classList.add('wrong');b.insertAdjacentHTML('beforeend','<span class="mark">✗</span>');}
    document.getElementById('after').innerHTML='<div class="why"><strong>'+(ok?S.ok:S.no)+'</strong>'+esc(q.e)+'</div>'+
      '<div class="actions"><button class="btn btn-sign" type="button" id="next">'+(last?S.score:S.next)+'</button></div>';
    var n=document.getElementById('next');
    n.addEventListener('click',function(){if(last)done();else{i++;show();}});
    n.focus({preventScroll:true});
  }

  function done(){
    var p=Math.round(right/qs.length*100),pass=p>=PASS,full=mode!=='missed';
    if(full)Store.saveBest(data.slug,p);
    // remember mistakes: add new ones, clear ones answered right
    var set=Store.missed(data.slug);
    answers.forEach(function(a){var at=set.indexOf(a.q.q);if(a.ok&&at>-1)set.splice(at,1);if(!a.ok&&at<0)set.push(a.q.q);});
    Store.setMissed(data.slug,set);
    var streak=Store.studied();
    var h='<div class="lane" aria-hidden="true"><span style="width:100%"></span></div>'+
      '<div class="result"><div class="score">'+p+'%</div>'+
      (pass&&full?'<div class="badge big" aria-hidden="true"><span>✓</span></div>':'')+'</div>'+
      '<p class="verdict '+(pass?'pass':'fail')+'">'+(pass?(full?S.passed(esc(data.name)):S.fixed):S.notYet)+'</p>'+
      '<p>'+S.got(right,qs.length)+
      (streak>1?' <span class="streak">🔥 '+streak+(ES?' ':'')+S.streak+'</span>':'')+'</p>';
    if(pass){
      h+='<div class="next"><img class="shield-img" src="https://otrnews.com/partners/mycdlcoach-shield.webp" alt="MyCDLCoach" width="44" height="44"><h3>'+S.passH+'</h3>'+
        '<p>'+S.passP+'</p>'+
        '<a class="btn btn-sign" href="'+track(LINKS.course,'pass')+'">'+S.passB+'</a>'+
        '<p class="alt">'+S.notReady+'<a href="'+track(LINKS.lounge,'pass')+'">'+S.lounge+'</a></p></div>';
    }else{
      h+='<div class="next"><img class="shield-img" src="https://otrnews.com/partners/mycdlcoach-shield.webp" alt="MyCDLCoach" width="44" height="44"><h3>'+S.failH+'</h3>'+
        '<p>'+S.failP+'</p>'+
        '<a class="btn btn-sign" href="'+track(LINKS.lounge,'fail')+'">'+S.lounge+'</a></div>';
    }
    h+='<div class="actions">'+
      (Store.missed(data.slug).length?'<button class="btn btn-ghost" type="button" id="fix">'+S.fix+' ('+Store.missed(data.slug).length+')</button>':'')+
      '<button class="btn btn-ghost" type="button" id="again">'+S.again+'</button>'+
      '<button class="btn btn-ghost" type="button" id="share">'+S.share+'</button>'+
      '<a class="btn btn-ghost" href="'+S.home+'">'+S.other+'</a></div>';
    var wrong=answers.filter(function(a){return !a.ok;});
    if(wrong.length){
      h+='<h3>'+S.review+'</h3><ul class="missed">';
      wrong.forEach(function(a){h+='<li><div>'+esc(a.q.q)+'</div>'+
        (mode==='exam'?'<div class="yours">'+S.yours+esc(a.choice)+'</div>':'')+
        '<div class="ans">'+esc(a.q.a)+'</div><div class="exp">'+esc(a.q.e)+'</div></li>';});
      h+='</ul>';
    }
    box.innerHTML=h;
    document.getElementById('again').addEventListener('click',menu);
    var f=document.getElementById('fix');if(f)f.addEventListener('click',function(){start('missed');});
    document.getElementById('share').addEventListener('click',function(){
      share(S.shareT(p,data.name));});
    box.scrollIntoView({behavior:'smooth',block:'start'});
    if(pass)confetti();
  }

  menu();
})();

// ===== Home page: progress, badges, question of the day =====
(function(){
  if(!window.TESTS)return;
  var s=Store.get(),best=s.best||{},passed=0,tried=0;
  window.TESTS.forEach(function(slug){
    var b=best[slug];if(b==null)return;tried++;
    var el=document.querySelector('[data-best="'+slug+'"]');if(el){el.textContent='Best: '+b+'%';el.hidden=false;}
    if(b>=PASS){passed++;var bd=document.querySelector('[data-badge="'+slug+'"]');if(bd)bd.hidden=false;}
  });
  var st=Store.streak(),dash=document.getElementById('dash');
  if(tried&&dash){
    var pct=Math.round(passed/window.TESTS.length*100);
    dash.innerHTML='<div class="dash-row"><strong>Your progress</strong>'+(st>0?'<span class="streak">🔥 '+st+'-day streak</span>':'')+'</div>'+
      '<div class="lane" aria-hidden="true"><span style="width:'+pct+'%"></span></div>'+
      '<p>You\'ve passed '+passed+' of '+window.TESTS.length+' tests. Progress is saved on this device.</p>';
    dash.hidden=false;
  }

  var box=document.getElementById('qotd-box');if(!box||!window.ALLQ)return;
  var d=new Date(),n=Math.floor(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())/864e5);
  var q=window.ALLQ[(n*7)%window.ALLQ.length],opts=shuffle([q.a].concat(q.w));
  var done=(s.qotd===today());
  var h='<p class="qotd-from">From the '+esc(q.n)+' test</p><p class="qotd-q" id="qq">'+esc(q.q)+'</p><div class="opts" role="group" aria-labelledby="qq">';
  opts.forEach(function(o){h+='<button class="opt" type="button">'+esc(o)+'</button>';});
  h+='</div><div id="qotd-after" aria-live="polite"></div>';
  box.innerHTML=h;
  var btns=box.querySelectorAll('.opt');
  function reveal(choice){
    btns.forEach(function(x){x.disabled=true;if(x.textContent===q.a)x.classList.add('right');});
    if(choice&&choice.textContent!==q.a)choice.classList.add('wrong');
    var ok=!choice||choice.textContent===q.a;
    document.getElementById('qotd-after').innerHTML='<div class="why"><strong>'+(choice?(ok?'Correct!':'Not quite.'):'Today\'s answer:')+'</strong>'+esc(q.e)+'</div>'+
      '<div class="actions"><a class="btn btn-sign" href="/'+q.t+'">Practice more '+esc(q.n)+'</a></div>';
  }
  btns.forEach(function(b){b.addEventListener('click',function(){var s2=Store.get();s2.qotd=today();Store.set(s2);Store.studied();reveal(b);});});
  if(done)reveal(null);
})();

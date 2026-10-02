// Where the results screen sends people. Swap in your exact MyCDLCoach links here.
var LINKS = {
  course: 'https://mycdlcoach.com',  // CDL Fast Track ($149) checkout or course page
  lounge: 'https://mycdlcoach.com'   // Free Driver's Lounge sign-up page
};
function track(url, result){return url+(url.indexOf('?')>-1?'&':'?')+'utm_source=cdlpermits&utm_medium=results&utm_campaign='+result;}

(function(){
  var data = window.QUIZ; if(!data) return;
  var box = document.getElementById('quiz');
  var PASS = 80, qs, i, right, missed;

  function shuffle(a){a=a.slice();for(var k=a.length-1;k>0;k--){var j=Math.floor(Math.random()*(k+1));var t=a[k];a[k]=a[j];a[j]=t;}return a;}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function saveBest(p){try{var k='best:'+data.slug;var b=parseInt(localStorage.getItem(k)||'0',10);if(p>b)localStorage.setItem(k,String(p));}catch(e){}}

  function start(){qs=shuffle(data.questions);i=0;right=0;missed=[];show();}

  function show(){
    var q=qs[i];
    var opts=shuffle([q.a].concat(q.w));
    var pct=Math.round(i/qs.length*100);
    var h='<div class="lane" aria-hidden="true"><span style="width:'+pct+'%"></span></div>'+
      '<p class="count">Question '+(i+1)+' of '+qs.length+', '+right+' correct so far</p>'+
      '<h2 id="qtext">'+esc(q.q)+'</h2><div class="opts" role="group" aria-labelledby="qtext">';
    opts.forEach(function(o){h+='<button class="opt" type="button">'+esc(o)+'</button>';});
    h+='</div><div id="after" aria-live="polite"></div>';
    box.innerHTML=h;
    var btns=box.querySelectorAll('.opt');
    btns.forEach(function(b){b.addEventListener('click',function(){answer(b,btns,q);});});
    btns[0].focus({preventScroll:true});
  }

  function answer(b,btns,q){
    var ok=b.textContent===q.a;
    btns.forEach(function(x){
      x.disabled=true;
      if(x.textContent===q.a){x.classList.add('right');x.insertAdjacentHTML('afterbegin','<span class="mark">✓</span>');}
    });
    if(ok){right++;}else{b.classList.add('wrong');b.insertAdjacentHTML('afterbegin','<span class="mark">✗</span>');missed.push(q);}
    var last=i===qs.length-1;
    document.getElementById('after').innerHTML=
      '<div class="why"><strong>'+(ok?'Correct.':'Not quite.')+'</strong>'+esc(q.e)+'</div>'+
      '<div class="actions"><button class="btn btn-sign" type="button" id="next">'+(last?'See my score':'Next question')+'</button></div>';
    var n=document.getElementById('next');
    n.addEventListener('click',function(){if(last){done();}else{i++;show();}});
    n.focus({preventScroll:true});
  }

  function done(){
    var p=Math.round(right/qs.length*100); saveBest(p);
    var pass=p>=PASS;
    var h='<div class="lane" aria-hidden="true"><span style="width:100%"></span></div>'+
      '<p class="count">'+esc(data.name)+' practice test complete</p>'+
      '<div class="score">'+p+'%</div>'+
      '<p class="verdict '+(pass?'pass':'fail')+'">'+(pass?'You would pass.':'Not passing yet.')+'</p>'+
      '<p>You got '+right+' of '+qs.length+' right. Most states require 80% to pass.</p>';
    if(pass){
      h+='<div class="next"><h3>Your next step: ELDT theory</h3>'+
        '<p>Before your CDL skills test, federal rules require Entry-Level Driver Training theory from a registered provider. MyCDLCoach Fast Track is FMCSA-certified, 100% online, and most students finish in under a day. Your certificate is uploaded to the FMCSA the same day.</p>'+
        '<a class="btn btn-sign" href="'+track(LINKS.course,'pass')+'">Get my ELDT certificate, $149</a>'+
        '<p class="alt">Not ready to pay? <a href="'+track(LINKS.lounge,'pass')+'">Join the free Driver\'s Lounge</a></p></div>';
    }else{
      h+='<div class="next"><h3>Get help reaching 80%</h3>'+
        '<p>Join the free MyCDLCoach Driver\'s Lounge. Ask working drivers about the questions that tripped you up, get study tips, and connect with people going through the same process.</p>'+
        '<a class="btn btn-sign" href="'+track(LINKS.lounge,'fail')+'">Join the free Driver\'s Lounge</a></div>';
    }
    h+='<div class="actions"><button class="btn btn-ghost" type="button" id="again">Take it again</button>'+
      '<a class="btn btn-ghost" href="/">Pick another test</a></div>';
    if(missed.length){
      h+='<h3>Review what you missed</h3><ul class="missed">';
      missed.forEach(function(q){h+='<li><div>'+esc(q.q)+'</div><div class="ans">'+esc(q.a)+'</div></li>';});
      h+='</ul>';
    }
    box.innerHTML=h;
    document.getElementById('again').addEventListener('click',start);
    box.scrollIntoView({behavior:'smooth',block:'start'});
  }

  start();
})();

// Best scores on the home page
(function(){
  document.querySelectorAll('[data-best]').forEach(function(el){
    try{var b=localStorage.getItem('best:'+el.getAttribute('data-best'));
      if(b){el.textContent='Your best: '+b+'%';el.hidden=false;}}catch(e){}
  });
})();


(function(){
  window._draftPhraseRendu = function(){
    var df=document.getElementById('draftForm'); if(!df) return;
    var box=document.getElementById('draftPhrase');
    if(!box){ box=document.createElement('div'); box.id='draftPhrase'; df.insertBefore(box, df.firstChild); }
    var titre=(document.getElementById('dfTitle')||{}).value||'';
    var quand=window._draftQuand||'y revenir un jour';
    var pl=function(cle,txt,vide){ return '<span class="ph-m'+(vide?' ph-vide':'')+'" data-dp2="'+cle+'">'+txt+'</span>'; };
    var h='Je garde une idée<br>'+pl('titre', titre||'le titre', !titre)
      +'<br><em>pour</em> '+pl('quand', quand, false);
    box.innerHTML='<div class="ph-txt">'+h+'</div><div class="ph-choix" id="draftChoix"></div>';
    box.querySelectorAll('[data-dp2]').forEach(function(el){ el.onclick=function(){ _draftChoix(el.getAttribute('data-dp2'), el); }; });
  };
  window._draftChoix = function(cle, el){
    var zone=document.getElementById('draftChoix'); if(!zone) return;
    document.querySelectorAll('#draftPhrase .ph-m').forEach(function(x){ x.classList.toggle('ph-on', x===el); });
    if(cle==='titre'){
      var v=(document.getElementById('dfTitle')||{}).value||'';
      zone.innerHTML='<div class="ph-lab">CE QUE TU GARDES</div><input class="ph-in" id="draftTitreIn" placeholder="une idée, un projet…" value="'+v.replace(/"/g,'&quot;')+'">';
      var i=zone.querySelector('#draftTitreIn');
      i.oninput=function(){ var t=document.getElementById('dfTitle'); if(t){ t.value=i.value; t.dispatchEvent(new Event('input',{bubbles:true})); }
        el.textContent=i.value||'le titre'; el.classList.toggle('ph-vide', !i.value); };
      i.onkeydown=function(e){ if(e.key==='Enter'){ e.preventDefault(); i.blur(); } };
      i.onblur=function(){ _draftPhraseRendu(); };
      setTimeout(function(){ try{i.focus();}catch(_){} },30);
    } else {
      var opts=['y revenir un jour','cette semaine','ce mois-ci','plus tard'];
      var cur=window._draftQuand||'y revenir un jour';
      zone.innerHTML='<div class="ph-lab">POUR Y REVENIR</div><div class="ph-opts">'
        + opts.map(function(o){ return '<button type="button" class="ph-o'+(o===cur?' on':'')+'" data-v="'+o+'">'+o+'</button>'; }).join('')+'</div>';
      zone.querySelectorAll('.ph-o').forEach(function(b){ b.onclick=function(){ window._draftQuand=b.dataset.v;
        try{ var map={'cette semaine':'5','ce mois-ci':'14','plus tard':'40','y revenir un jour':'40'}; var d=map[b.dataset.v];
          if(d){ var chip=document.querySelector('#dfDueChips .chip[data-d="'+d+'"]'); if(chip)chip.click(); } }catch(_){}
        _draftPhraseRendu();
        try{ var m=document.querySelector('#draftPhrase .ph-m[data-dp2=quand]'); if(m)_draftChoix('quand', m); }catch(_){}
      }; });
    }
  };
  function go(){ try{ var cs=document.getElementById('createSheet'); if(cs && cs.getAttribute('data-kind')==='draft') _draftPhraseRendu(); }catch(_){} }
  document.addEventListener('click', function(e){ var t=e.target&&e.target.closest?e.target.closest('#createSheet .tile[data-kind="draft"]'):null; if(t) setTimeout(go,220); }, false);
  var cb=document.getElementById('createBtn'); if(cb) cb.addEventListener('click', function(){ setTimeout(go,320); });
})();

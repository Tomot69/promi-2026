(function(){try{
var obs=new MutationObserver(function(muts){muts.forEach(function(m){var el=m.target;
  if(el.classList&&el.classList.contains('tuto-fond')&&el.classList.contains('show')){
    if(el.__lastShown&&Date.now()-el.__lastShown<300)return;el.__lastShown=Date.now();
    for(var _i=0;_i<5;_i++)el.classList.remove('gs'+_i);
    el.classList.add('gs'+Math.floor(Math.random()*5));
  }});});
document.querySelectorAll('.tuto-fond').forEach(function(e){obs.observe(e,{attributes:true,attributeFilter:['class']});});
}catch(e){}})();
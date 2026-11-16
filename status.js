// Progressive enhancement: refresh status badges from the live GitHub issue (labels + 👍/👎).
(function(){
  var REPO="jgridifier/nitro-xml";
  document.querySelectorAll("[data-status-for]").forEach(function(el){
    var n=el.getAttribute("data-status-for"); if(!n) return;
    fetch("https://api.github.com/repos/"+REPO+"/issues/"+n,{headers:{Accept:"application/vnd.github+json"}})
      .then(function(r){return r.ok?r.json():null}).then(function(i){
        if(!i) return;
        var L=(i.labels||[]).map(function(l){return l.name}), up=(i.reactions||{})["+1"]||0, dn=(i.reactions||{})["-1"]||0, s=null;
        if(i.state==="closed"&&i.state_reason==="completed") s="Shipped";
        else if(i.state==="closed"||L.indexOf("declined")>=0||(dn>0&&up===0)) s="Declined";
        else if(L.indexOf("building")>=0) s="Building";
        else if(L.indexOf("approved")>=0||up>0) s="Approved";
        if(s){el.textContent=s; el.className="badge s-"+s.toLowerCase();}
      }).catch(function(){});
  });
})();

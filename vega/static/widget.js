define(["@jupyter-widgets/base","jupyter-vega"],((e,t)=>(()=>{"use strict";var n={891:function(e,t,n){var r=this&&this.__awaiter||function(e,t,n,r){return new(n||(n=Promise))((function(i,o){function s(e){try{l(r.next(e))}catch(e){o(e)}}function c(e){try{l(r.throw(e))}catch(e){o(e)}}function l(e){var t;e.done?i(e.value):(t=e.value,t instanceof n?t:new n((function(e){e(t)}))).then(s,c)}l((r=r.apply(e,t||[])).next())}))};Object.defineProperty(t,"__esModule",{value:!0}),t.VegaWidget=void 0;const i=n(146),o=n(407);class s extends i.DOMWidgetView{constructor(){super(...arguments),this.viewElement=document.createElement("div"),this.errorElement=document.createElement("div")}render(){return r(this,void 0,void 0,(function*(){this.el.appendChild(this.viewElement),this.errorElement.style.color="red",this.el.appendChild(this.errorElement);const e=()=>r(this,void 0,void 0,(function*(){const e=JSON.parse(this.model.get("_spec_source")),t=JSON.parse(this.model.get("_opt_source"));if(null!=e)try{const n=yield(0,o.vegaEmbed)(this.viewElement,e,Object.assign({loader:{http:{credentials:"same-origin"}}},t));this.result&&this.result.finalize(),this.result=n,this.send({type:"display"})}catch(e){this.result&&this.result.finalize(),console.error(e)}})),t=e=>r(this,void 0,void 0,(function*(){const t=this.result;if(null==t)throw new Error("Internal error: no view attached to widget");const n=new Function("datum","return ("+(e.remove||"false")+")"),r=e.insert||[],i=t.view.changeset().remove(n).insert(r);yield t.view.change(e.key,i).runAsync()})),n=e=>r(this,void 0,void 0,(function*(){for(const n of e.updates)yield t(n)}));this.model.on("change:_spec_source",e),this.model.on("change:_opt_source",e),this.model.on("msg:custom",(e=>{const t=function(e){return"update"!=e.type?null:e}(e);null!=t&&n(t).catch((e=>{this.errorElement.textContent=String(e),console.error(e)}))})),yield e()}))}}t.VegaWidget=s},146:t=>{t.exports=e},407:e=>{e.exports=t}},r={};return function e(t){var i=r[t];if(void 0!==i)return i.exports;var o=r[t]={exports:{}};return n[t].call(o.exports,o,o.exports,e),o.exports}(891)})()));
//# sourceMappingURL=widget.js.map
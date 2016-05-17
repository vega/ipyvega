var spec = {spec};
var selector = "{selector}";
var type = "{type}";

console.log(spec);
console.log(selector);
console.log(type);

var output_area = this;

require(['nbextensions/vega/index'], function(vega) {{
  vega.render(selector, spec, type, output_area);
}});

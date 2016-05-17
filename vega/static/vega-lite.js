var spec = %s;
var selector = "%s";
var type = "%s";

var output_area = this;

require(['nbextensions/vega/index'], function(vega) {
  vega.render(selector, spec, type, output_area);
});

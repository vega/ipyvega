var spec = {spec};
var opt = {opt};
var selector = "{selector}";
var type = "{type}";

var output_area = this;

require(['nbextensions/jupyter-vega/index'], function(vega) {{
  vega.render(selector, spec, type, opt, output_area);
}}, function (err) {{
  if (err.requireType !== 'scripterror') {{
    throw(err);
  }}
}});

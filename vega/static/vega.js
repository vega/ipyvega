var spec = {spec};
var selector = "{selector}";
var type = "{type}";

var output_area = this;

try {{
  require(['nbextensions/jupyter-vega/index'], function(vega) {{
    vega.render(selector, spec, type, output_area);
  }});
}} catch (e) {{
}}

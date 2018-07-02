var spec = {spec};
var opt = {opt};
var type = "{type}";
var id = "{id}";

var output_area = this;

require(["nbextensions/jupyter-vega/index"], function(vega) {{
  var target = document.createElement("div");
  target.id = id;
  target.className = "vega-embed";

  var style = document.createElement("style");
  style.textContent = [
    ".vega-embed .error p {{",
    "  color: firebrick;",
    "  font-size: 14px;",
    "}}",
  ].join("\\n");

  // element is a jQuery wrapped DOM element inside the output area
  // see http://ipython.readthedocs.io/en/stable/api/generated/\
  // IPython.display.html#IPython.display.Javascript.__init__
  element[0].appendChild(target);
  element[0].appendChild(style);

  vega.render("#" + id, spec, type, opt, output_area);
}}, function (err) {{
  if (err.requireType !== "scripterror") {{
    throw(err);
  }}
}});

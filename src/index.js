require('./embed.css');

var d3 = require('d3');
var embed = require("vega-embed");

d3.selectAll('.vega-embed').each(function() {
  var sel = d3.select(this);
  var type = sel.attr('data-type');

  if (type) {
    var embedSpec = {
      mode: type,
      spec: JSON.parse(sel.text())
    }

    embed(sel.node(), embedSpec, function(error, result) {
      // Callback receiving the View instance and parsed Vega spec
      // result.view is the View, which resides under the '#vis' element
    });
  }
});

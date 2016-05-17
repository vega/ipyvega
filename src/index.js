// require('./embed.css');

var embed = require('vega-embed');
var $ = require('jquery');
var events = require('base/js/events');

function render(selector, spec, type, output_area) {
  console.log(selector, spec, type, output_area);
  var el = $.find(selector).first();
  if (type) {
    var embedSpec = {
      mode: type,
      spec: spec
    }

    embed(el[0], embedSpec, function(error, result) {
      console.log(result)
      // Callback receiving the View instance and parsed Vega spec
      // result.view is the View, which resides under the '#vis' element
      // Grab the base64 encoded png here and send it to output_area.append_output
    });
  }
}

exports.render = render;

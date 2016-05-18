// require('./embed.css');

var embed = require('vega-embed');
var $ = require('jquery');
var events = require('base/js/events');

function render(selector, spec, type, output_area) {
  var el = $.find(selector);
  if (type) {
    var embedSpec = {
      mode: type,
      spec: spec
    }

    embed(el[0], embedSpec, function(error, result) {
      var imageData = result.view.toImageURL();
      var output = {
          data: {
            "image/png": imageData.split(",")[1]
          },
          metadata: {},
          output_type: "display_data"
      };
      output_area.outputs.append(output);
    });
  }
}

exports.render = render;

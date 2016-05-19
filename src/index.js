var embed = require('vega-embed');
var $ = require('jquery');
var events = require('base/js/events');

// Polyfill findIndex if needed
if (!Array.prototype.findIndex) {
  Array.prototype.findIndex = function(predicate) {
    if (this === null) {
      throw new TypeError('Array.prototype.findIndex called on null or undefined');
    }
    if (typeof predicate !== 'function') {
      throw new TypeError('predicate must be a function');
    }
    var list = Object(this);
    var length = list.length >>> 0;
    var thisArg = arguments[1];
    var value;

    for (var i = 0; i < length; i++) {
      value = list[i];
      if (predicate.call(thisArg, value, i, list)) {
        return i;
      }
    }
    return -1;
  };
}

function javascriptIndex(selector, outputs) {
  // Return the index in the output array of the JS repr of this viz
  var index = outputs.findIndex(function(item, index, array) {
    if (item['metadata']['jupyter-vega']===selector &&
        item['data']['application/javascript']!==undefined) {
      return true;
    } else {
      return false;
    }
  });
  return index;
}

function imageIndex(selector, outputs) {
  // Return the index in the output array of the PNG repr of this viz
  var index = outputs.findIndex(function(item, index, array) {
    if (item['metadata']['jupyter-vega']===selector &&
        item['data']['image/png']!==undefined) {
      return true;
    } else {
      return false;
    }
  });
  return index;
}

function render(selector, spec, type, output_area) {
  if (type) {
    var embedSpec = {
      mode: type,
      spec: spec
    };

    // Find the indices of this visualizations JS and PNG
    // representation.
    var imgIndex = imageIndex(selector, output_area.outputs);
    var jsIndex = javascriptIndex(selector, output_area.outputs);

    // If we have already rendered a static image, don't render
    // the JS version or append a new PNG version
    if (imgIndex >- 1 && jsIndex >- 1 && imgIndex === (jsIndex+1)) {
      return;
    }

    // Never been rendered, so render JS and append the PNG to the
    // outputs for the cell
    var el = $.find(selector);
    embed(el[0], embedSpec, function(error, result) {
      var imageData = result.view.toImageURL();
      if (output_area!==undefined) {
        var output = {
            data: {
              'image/png': imageData.split(',')[1]
            },
            metadata: {'jupyter-vega': selector},
            output_type: 'display_data'
        };
        // This appends the PNG output, but doesn't render it this time
        // as the JS version will be rendered already.
        output_area.outputs.push(output);
      }
    });
  }
}

exports.render = render;

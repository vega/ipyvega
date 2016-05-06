require('./embed.css');

var embed = require('vega-embed');
var $ = require('jquery');
var events = require('base/js/events');

function render_all() {
  $('.vega-embed').each(function(i, el) {
    render($(el));
  });
}

function render_one(event, type, value, metadata, $toinsert) {
  var el = $toinsert.find('.vega-embed');
  render(el);
}

function render(el) {
  var type = el.attr('data-type');

  if (type) {
    var embedSpec = {
      mode: type,
      spec: JSON.parse(el.text())
    }

    embed(el[0], embedSpec, function(error, result) {
      // Callback receiving the View instance and parsed Vega spec
      // result.view is the View, which resides under the '#vis' element
    });
  }
}

function load_extension() {
  events.on("notebook_loaded.Notebook", render_all);
  events.on("kernel_ready.Kernel", render_all);
  events.on("output_appended.OutputArea", render_one);
  render_all();
}

exports.load_jupyter_extension = load_extension;
exports.load_ipython_extension = load_extension;

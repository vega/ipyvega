console.log("bar")

require.config({
  paths: {
    d3: "%(path)s/d3.min",
    vegalite: "%(path)s/vega.min",
    vega: "%(path)s/vega-lite.min",
    embed: "%(path)s/vega-embed.min"
  }
  // shim: {
  //   vega: {
  //     exports: 'vg',
  //     deps: ['d3']
  //   }
  // }
});

require(['d3', 'vega', 'vegalite', 'embed'], function(d3, vg, vl, embed){

  alert("hello from the inside")

  console.log("test");

  debugger;

  d3.selectAll('.vega-embed').each(function() {
    var sel = d3.select(this);
    var type = sel.attr('data-type');

    if (type) {
      var embedSpec = {
        mode: type,
        spec: sel.text()
      }

      vg.embed(sel.node(), embedSpec, function(error, result) {
        // Callback receiving the View instance and parsed Vega spec
        // result.view is the View, which resides under the '#vis' element
      });
    }
  });
}, function(err) {
  console.warn(err);
});

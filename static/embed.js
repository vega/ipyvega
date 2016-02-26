d3.selectAll('.vega-embed').each(function() {
  const sel = d3.select(this);
  const type = sel.attr('data-type');

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

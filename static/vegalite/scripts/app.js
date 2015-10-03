function parse(spec) {
  vg.parse.spec(spec, function(chart) {
    chart({el:"#vis"}).update(); });
}

var vlDataSpec = $.extend(vlData, vlSpec);

var vgSpec = vl.compile(vlDataSpec);

parse(vgSpec);

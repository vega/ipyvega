vlSpec.data = {values: vlData};

vl.util.extend(vlSpec, {
	config: {
		cell: {
      width: 500,
      height: 350
    }
  }
});

var embedSpec = {
  mode: "vega-lite",
  spec: vlSpec
}

vg.embed("#vis", embedSpec, function(error, result) {
  // Callback receiving the View instance and parsed Vega spec
  // result.view is the View, which resides under the '#vis' element
});

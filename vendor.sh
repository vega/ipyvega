#!/bin/bash

npm install

cp node_modules/d3/d3.js static/
cp node_modules/d3/d3.min.js static/

cp node_modules/vega/vega.js static/
cp node_modules/vega/vega.min.js static/

cp node_modules/vega-lite/vega-lite.js static/
cp node_modules/vega-lite/vega-lite.min.js static/

cp node_modules/vega-embed/vega-embed.js static/
cp node_modules/vega-embed/vega-embed.min.js static/

var webpack = require('webpack');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'index.js',
    path: __dirname + '/vega3/static',
    libraryTarget: 'amd'
  },
  devtool: 'source-map',
  module: {
    loaders: [
        { test: /\.json$/, loader: 'json-loader' },
        { test: /\.css$/, loader: 'style-loader!css-loader' },
    ]
  },
  externals: {
    'base/js/events': 'base/js/events',
    'jquery': 'jquery'
  }
};

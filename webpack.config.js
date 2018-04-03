var webpack = require('webpack');

module.exports = {
  entry: './src/index.ts',
  output: {
    filename: 'index.js',
    path: __dirname + '/vega3/static',
    libraryTarget: 'amd'
  },
  resolve: {
    extensions: [".ts", ".tsx", ".js"]
  },
  devtool: 'source-map',
  module: {
    loaders: [
        { test: /\.json$/, loader: 'json-loader' },
        { test: /\.css$/, loader: 'style-loader!css-loader' },
        { test: /\.tsx?$/, loader: 'awesome-typescript-loader', query: {useCache: true} }
    ]
  },
  externals: {
    'base/js/events': 'base/js/events',
    'jquery': 'jquery'
  }
};

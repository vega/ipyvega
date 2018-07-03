var webpack = require('webpack');

module.exports = {
  entry: './src/index.ts',
  output: {
    filename: 'index.js',
    path: __dirname + '/vega/static',
    library: 'nbextensions/jupyter-vega/index',
    libraryTarget: 'amd'
  },
  externals: ['@jupyter-widgets/base'],
  resolve: {
    extensions: [".ts", ".tsx", ".js"]
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: 'ts-loader'
      },
      {
        test: /\.css$/,
        use: [
          { loader: "css-loader" }
        ]
      }
    ]
  }
};

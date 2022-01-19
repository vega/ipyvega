const version = require('./package.json').version;
const path = require('path');
const FileManagerPlugin = require('filemanager-webpack-plugin');

const outputPath = __dirname + "/vega/static";

const commonConfig = {
  resolve: {
    extensions: [".ts", ".tsx", ".js"]
  },
  devtool: "source-map",
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: "ts-loader"
      }
    ]
  },
  externals: ["@jupyter-widgets/base"],
  plugins: [
    new FileManagerPlugin({
      events: {
        onEnd: {
          copy: [
            { source: './src/vega.js', destination: outputPath + '/vega.js' },
            { source: outputPath + '/*', destination: './dist' }
          ]
        }
      }
    })
  ]
};


module.exports = [
  // the main vega extension
  Object.assign({}, commonConfig, {
    entry: "./src/index.ts",
    output: {
      filename: "index.js",
      path: outputPath,
      libraryTarget: "amd",
      publicPath: 'https://unpkg.com/jupyter-vega@' + version + '/dist/'
    }
  }),
  // the widget extension
  Object.assign({}, commonConfig, {
    entry: "./src/widget.ts",
    output: {
      filename: "widget.js",
      path: outputPath,
      libraryTarget: "amd"
    }
  })
];

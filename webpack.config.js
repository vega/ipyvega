const version = require('./package.json').version;
const path = require('path');
const FileManagerPlugin = require('filemanager-webpack-plugin');

module.exports = [
  {
    entry: "./src/index.ts",
    output: {
      filename: "index.js",
      path: path.resolve(__dirname, "vega", "static"),
      libraryTarget: "amd",
      publicPath: 'https://unpkg.com/jupyter-vega@' + version + '/dist/'
    },
    resolve: { extensions: [".ts", ".tsx", ".js"] },
    module: { rules: [{ test: /\.tsx?$/, loader: "ts-loader" }] },
    externals: ["@jupyter-widgets/base"],
    devtool: "source-map",
    plugins: [
      new FileManagerPlugin({
        events: {
          onEnd: { 
            copy: [
              { source: './src/vega.js', destination: './vega/static/vega.js' },
              { source: './vega/static/*', destination: './dist' }
            ]
          }
        }
      })
    ]
  }
];

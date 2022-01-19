const version = require('./package.json').version;
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
    },
    externals: ["@jupyter-widgets/base"]
  }),
  // the widget extension
  Object.assign({}, commonConfig, {
    entry: "./src/widget.ts",
    output: {
      filename: "widget.js",
      path: outputPath,
      libraryTarget: "amd"
    },
    externals: {
      "@jupyter-widgets/base": "@jupyter-widgets/base",
      "./index": "jupyter-vega"
    }
  })
];

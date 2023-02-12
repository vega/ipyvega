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
    entry: "./src/extension.ts",
    output: {
      filename: "extension.js",
      path: outputPath,
      libraryTarget: "amd",
    },
    externals: ["@jupyter-widgets/base"]
  }),
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
  // the index extension
  Object.assign({}, commonConfig, {
    entry: "./src/index.ts",
    output: {
      filename: "index.js",
      path: outputPath,
      libraryTarget: "amd"
    },
    externals: ["@jupyter-widgets/base"]
  }),
  Object.assign({}, commonConfig, {
    entry: "./src/labplugin.ts",
    output: {
      filename: "labplugin.js",
      path: outputPath,
      libraryTarget: "amd"
    },
    externals: ["@jupyter-widgets/base"]
  }),
];

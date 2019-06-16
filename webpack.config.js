var webpack = require("webpack");

module.exports = [
  // the main vega extension
  {
    entry: "./src/index.ts",
    output: {
      filename: "index.js",
      path: __dirname + "/vega/static",
      library: "nbextensions/jupyter-vega/index",
      libraryTarget: "amd"
    },
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
    }
  },
  // the widget extension
  {
    entry: "./src/widget.ts",
    output: {
      filename: "widget.js",
      path: __dirname + "/vega/static",
      libraryTarget: "amd"
    },
    externals: {
      "@jupyter-widgets/base": "@jupyter-widgets/base",
      "./index": "nbextensions/jupyter-vega/index"
    },
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
    }
  }
];

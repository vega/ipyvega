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
  }
};

const outputPath = __dirname + "/vega/static";
const outputLibraryTarget = "amd";

module.exports = [
  // the main vega extension
  Object.assign({}, commonConfig, {
    entry: "./src/index.ts",
    output: {
      filename: "index.js",
      library: "nbextensions/jupyter-vega/index",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    }
  }),
  // the widget extension
  Object.assign({}, commonConfig, {
    entry: "./src/widget.ts",
    output: {
      filename: "widget.js",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    },
    externals: {
      "@jupyter-widgets/base": "@jupyter-widgets/base",
      "./index": "nbextensions/jupyter-vega/index"
    }
  })
];

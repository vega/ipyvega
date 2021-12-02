const version = require('./package.json').version;
const path = require('path');

module.exports = [
  {
    entry: "./src/index.ts",
    output: {
      filename: "index.js",
      path: path.resolve(__dirname, "dist"),
      libraryTarget: "amd",
      publicPath: 'https://unpkg.com/jupyter-vega@' + version + '/dist/'
    },
    resolve: { extensions: [".ts", ".tsx", ".js"] },
    module: { rules: [{ test: /\.tsx?$/, loader: "ts-loader" }] },
    externals: ["@jupyter-widgets/base"],
    devtool: "source-map"
  }
];

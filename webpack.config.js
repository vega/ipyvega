module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'vega/static/embed.js',
    library: "IPythonVega",
    libraryTarget: "umd"
  },
  module: {
    loaders: [
      { test: /\.css$/, loader: 'style-loader!css-loader' },
    ]
  }
};
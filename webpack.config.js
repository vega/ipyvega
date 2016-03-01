module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'static/embed.js'
  },
  module: {
    loaders: [
      { test: /\.css$/, loader: 'style-loader!css-loader' },
    ]
  }
};
// webpack v4

var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,

  entry: './frontend/static/js/index',

  output: {
      path: path.resolve('./frontend/static/bundles/'),
      filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],
  module: {
    rules: [      
        {
          test: /\.jsx$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
          }
        },
        {
          test: /\.less$/,
          exclude: /node_modules/,
          use: [{
            loader: 'style-loader' // creates style nodes from JS strings
            }, {
            loader: 'css-loader', // translates CSS into CommonJS
            }, {
            loader: 'less-loader' // compiles Less to CSS
            }]
        },
        {
          test: /\.css$/,
          use: [{
              loader : 'style-loader'
            },{
              loader: 'css-loader'
            }]
        },
        {
          test: /\.(gif|png|jpg|svg)$/,
          use: [
            {
              loader: 'url-loader',
              options: {
              },
            },
          ],
        }     
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
 watchOptions: {
        poll: true
  }
};
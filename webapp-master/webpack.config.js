const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const HtmlPlugin = require("html-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const HtmlIncludeAssetsPlugin = require("html-webpack-include-assets-plugin");
const cesiumSource = 'node_modules/cesium/Source';
const cesiumWorkers = '../Build/Cesium/Workers';

const config = {
    entry:  __dirname + '/src/js/index.js',
    output: {
        path: 'C:\\Users\\e348829\\dev\\fullstack-docker\\server-master\\static',
        filename: 'bundle.js',
	    publicPath: '/static',
	    sourcePrefix: ''
    },
	amd: {
        toUrlUndefined: true
    },
    node: {
        fs: 'empty'
    },
	resolve: {
        extensions: [".js", ".jsx", ".css"],
	    alias: {
            cesium$: 'cesium/Cesium',
            cesium: 'cesium/Source'
        }
    },
    module: {
        rules: [
            {
                test: /\.jsx?/,
                exclude: /node_modules/,
                use: 'babel-loader'
            },
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: 'css-loader',
                })
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: [
	                {
		                loader: 'file-loader',
                        options: {
		                    name: '/img/[name].[ext]',
                        }
	                }

                ]
            }
        ]
    },
    plugins: [
        new ExtractTextPlugin('styles.css'),
        new CopyWebpackPlugin([
            {
                from: path.join(cesiumSource, cesiumWorkers),
                to: 'Workers'
            },
            {
                from: path.join(cesiumSource, 'Assets'),
                to: 'Assets'
            },
            {
                from: path.join(cesiumSource, 'Widgets'),
                to: 'Widgets'
            }
        ]),
        new webpack.DefinePlugin({
            CESIUM_BASE_URL: JSON.stringify('static/')
        })
    ]
};

module.exports = config;

require('babel-register')
const chai = require('chai')
chai.config.includeStack = true
global.expect = chai.expect
exports.config = require('./config.js').default

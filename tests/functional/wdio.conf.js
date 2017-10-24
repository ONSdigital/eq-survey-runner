//require('babel-register');
const config = require('./config');
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');
chai.config.includeStack = true;
chai.Should();
chai.use(chaiAsPromised);

global.expect = chai.expect;

exports.config = config;

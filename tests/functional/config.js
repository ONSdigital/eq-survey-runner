import {paths} from '../../gulp/paths'
import {chrome, chromeNoJS, firefox, ie11, ie10, ie9, ie8} from './capabilities'

var argv = require('yargs').argv
var browserstack = require('browserstack-local');


let config = {
  services: ['selenium-standalone'],
  // Level of logging verbosity: silent | verbose | command | data | result | error
  logLevel: 'error',
  coloredLogs: true,
  bail: 1,
  screenshotPath: paths.test.errorShots,
  baseUrl: process.env.BASEURL,
  waitforTimeout: 2000,
  updateJob: true,
  specs: [`${paths.test.wdioSpec}/**/*.spec.js`],
  suites: {
    core: [
      `${paths.test.wdioSpec}/*.spec.js`
    ],
    census: [
      `${paths.test.wdioSpec}/census/**/*.spec.js`
    ],
    ukis: [
      `${paths.test.wdioSpec}/ukis/**/*.spec.js`
    ]
  },
  sync: true,
  connectionRetryTimeout: 5000,
  connectionRetryCount: 3,
  capabilities: [chrome],
  framework: 'mocha',
  reporters: ['spec'],
  mochaOpts: {
    ui: 'bdd',
    compilers: ['js:babel-core/register'],
    timeout: 120000
  }
}

const sauceLabsConfig = {
  services: ['sauce'],
  sauceConnect: true,
  user: process.env.SAUCE_USERNAME,
  key: process.env.SAUCE_ACCESS_KEY,
  capabilities: [firefox]
}

const browserStackConfig = {
  logLevel: 'error',
  coloredLogs: true,
  bail: 1,
  screenshotPath: './errorShots/',
  waitforTimeout: 10000,
  connectionRetryTimeout: 90000,
  connectionRetryCount: 3,
  baseUrl: process.env.BASEURL,
  specs: [`${paths.test.wdioSpec}/**/*.spec.js`],
  suites: {
    core: [
      `${paths.test.wdioSpec}/*.spec.js`
    ],
    census: [
      `${paths.test.wdioSpec}/census/**/*.spec.js`
    ],
    ukis: [
      `${paths.test.wdioSpec}/ukis/**/*.spec.js`
    ]
  },
  user: process.env.BROWSERSTACK_USERNAME,
  key: process.env.BROWSERSTACK_ACCESS_KEY,
  updateJob: false,
  capabilities: [{
    browser: 'chrome',
    name: 'chrome_local',
    build: 'master 2',
    project: 'EQ Survey Runner',
    'browserstack.local': true,
    'browserstack.localIdentifier': process.env.BROWSERSTACK_LOCAL_IDENTIFIER
  }],
  maxInstances: 4,
  framework: 'mocha',
  reporters: ['spec'],
  mochaOpts: {
    ui: 'bdd',
    compilers: ['js:babel-core/register'],
    timeout: 240000
  },

  // Code to start browserstack local before start of test
  onPrepare: function (config, capabilities) {
    console.log("Connecting local");
    return new Promise(function(resolve, reject){
      exports.bs_local = new browserstack.Local();
      exports.bs_local.start({'key': config.key }, function(error) {
        if (error) return reject(error);
        console.log('Connected. Now testing...');

        resolve();
      });
    });
  },

  // Code to stop browserstack local after end of test
  onComplete: function (capabilties, specs) {
    exports.bs_local.stop(function() {});
  }
}

if (process.env.TRAVIS === 'true') {
  config = {
    ...browserStackConfig
  }
} else {
  if (argv.sauce) {
    config = {
      ...config,
      ...sauceLabsConfig
    }
  } else if (argv.browserstack) {
      config = {
      ...browserStackConfig
    }
  }
}

export default config

const paths = require('./paths');
const capabilities = require('./capabilities');
const argv = require('yargs');
const chaiAsPromised = require('chai-as-promised');

let config = {
  services: ['selenium-standalone'],
  // Level of logging verbosity: silent | verbose | command | data | result | error
  logLevel: 'error',
  coloredLogs: true,
  bail: 1,
  baseUrl: process.env.BASEURL,
  waitforTimeout: 2000,
  updateJob: true,
  specs: [`${paths.test.wdioSpec}/**/*.spec.js`],
  suites: {
    core: [
      `${paths.test.wdioSpec}/*.spec.js`
    ],
    census: [
      `${paths.test.wdioSpec}/census/*.spec.js`
    ],
    components: [
      `${paths.test.wdioSpec}/components/*.spec.js`
    ],
    features: [
      `${paths.test.wdioSpec}/features/**/*.spec.js`
    ],
    ukis: [
      `${paths.test.wdioSpec}/ukis/*.spec.js`
    ]
  },
  sync: false,
  connectionRetryTimeout: 5000,
  connectionRetryCount: 3,
  capabilities: [capabilities.chrome],
  framework: 'mocha',
  reporters: ['spec'],
  mochaOpts: {
    ui: 'bdd',
    timeout: 12000000
  },
  before: function(capabilities, specs) {
    // Allow chaining of browser promises with chai assertions
    chaiAsPromised.transferPromiseness = browser.transferPromiseness;
  },
  afterTest: function(test) {
    // Dump page source on failure to help with debugging tests

  }
};

const browserStackConfig = {
  services: ['browserstack'],
  user: process.env.BROWSERSTACK_USER,
  key: process.env.BROWSERSTACK_ACCESS_KEY,
  browserstackLocal: true
};

const phantomjsConfig = Object.assign(
  {},
  config,
  {
    services: ['phantomjs'],
    waitforTimeout: 3000,
    capabilities: [capabilities.phantomjs],
    maxInstances: 4,
    phantomjsOpts: {
      ignoreSslErrors: true
    },
    before: function() {
      chaiAsPromised.transferPromiseness = browser.transferPromiseness;
      browser.setViewportSize({
        width: 1280,
        height: 1024
      });
    }
  }
);

const chromeHeadlessConfig = Object.assign(
  {},
  config,
  {
    capabilities: [capabilities.chromeHeadless]
  }
);

if (process.env.TRAVIS === 'true') {
  config = chromeHeadlessConfig;

} else {
  if (argv.browserstack) {
    config = Object.assign(config, browserStackConfig);
  } else if (argv.headless) {
    config = Object.assign(config, phantomjsConfig);
  }
}

module.exports = config;

import {paths} from '../../gulp/paths'
import {chrome, firefox, phantomjs} from './capabilities'
import {argv} from 'yargs'

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
    timeout: 12000000
  },
  afterTest: function(test) {
    // Dump page source on failure to help with debugging tests
    if (!test.passed) {
      console.log('\'' + test.title + '\' failed. Dumping page source for url \'%s\'', browser.url().value)
      console.log(browser.getSource())
    }
  }
}

const sauceLabsConfig = {
  services: ['sauce'],
  sauceConnect: true,
  user: process.env.SAUCE_USERNAME,
  key: process.env.SAUCE_ACCESS_KEY,
  capabilities: [firefox]
}

const phantomjsConfig = {
  services: ['phantomjs'],
  waitforTimeout: 3000,
  capabilities: [phantomjs],
  maxInstances: 4,
  phantomjsOpts: {
    ignoreSslErrors: true
  },
  before: function() {
    browser.setViewportSize({
      width: 1280,
      height: 1024
    })
  }
}

if (process.env.TRAVIS === 'true') {
  config = {
    ...config,
    ...phantomjsConfig,
    logLevel: 'silent'
  }
} else {
  if (argv.sauce) {
    config = {
      ...config,
      ...sauceLabsConfig
    }
  } else if (argv.headless) {
    config = {
      ...config,
      ...phantomjsConfig
    }
  }
}

export default config

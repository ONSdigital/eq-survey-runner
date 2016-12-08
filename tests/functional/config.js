import {paths} from '../../gulp/paths'
import {chrome, firefox, ie11, ie10, ie9, ie8} from './capabilities'

var argv = require('yargs').argv

let config = {
  services: ['selenium-standalone'],
  // Level of logging verbosity: silent | verbose | command | data | result | error
  logLevel: 'error',
  coloredLogs: true,
  screenshotPath: paths.test.errorShots,
  baseUrl: process.env.BASEURL,
  waitforTimeout: 20000,
  updateJob: true,
  specs: [`${paths.test.wdioSpec}/**/*.spec.js`],
  suites: {
    core: [
      `${paths.test.wdioSpec}/*.spec.js`
    ],
    census: [
      `${paths.test.wdioSpec}/census/**/*.spec.js`
    ]
  },
  sync: true,
  connectionRetryTimeout: 5000,
  connectionRetryCount: 3,
  capabilities: [{
    name: 'Chrome (local)',
    browserName: 'chrome',
    maxInstances: 2
  }],
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

if (process.env.TRAVIS === 'true') {
  config = {
    ...config,
    logLevel: 'silent',
    capabilities: [chrome]
  }
} else {
  if (argv.sauce) {
    config = {
      ...config,
      ...sauceLabsConfig
    }
  }
}

export default config

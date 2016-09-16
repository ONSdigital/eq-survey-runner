import {paths} from '../../gulp/paths'
import {chrome, firefox, ie11, ie10, ie9, ie8} from './capabilities'

const useLocalSauceLabs = process.env.SAUCELABS === 'true' || false

let config = {
  services: ['selenium-standalone'],
  // Level of logging verbosity: silent | verbose | command | data | result | error
  logLevel: 'command',
  maxInstances: 1,
  coloredLogs: true,
  screenshotPath: paths.test.errorShots,
  baseUrl: process.env.BASEURL,
  waitforTimeout: 20000,
  updateJob: true,
  specs: [`${paths.test.wdioSpec}/**/*.spec.js`],
  sync: true,
  capabilities: [{
    name: 'Chrome (local)',
    browserName: 'chrome'
  }],
  framework: 'mocha',
  reporters: ['dot', 'spec'],
  mochaOpts: {
    ui: 'bdd',
    compilers: ['js:babel-core/register'],
    timeout: 60000
  }
}

const sauceLabsConfig = {
  services: ['sauce'],
  sauceConnect: true,
  user: process.env.SAUCE_USERNAME,
  key: process.env.SAUCE_ACCESS_KEY,
  capabilities: [chrome, ie11]
}

if (process.env.TRAVIS === 'true') {
  config = {
    ...config,
    ...sauceLabsConfig,
    logLevel: 'debug',
    capabilities: [chrome]
  }
} else {
  if (useLocalSauceLabs) {
    config = {
      ...config,
      ...sauceLabsConfig
    }
  }
}

export default config

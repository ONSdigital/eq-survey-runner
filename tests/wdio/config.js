import {paths} from '../../gulp/paths'
import {chrome, firefox, ie11, ie10, ie9, ie8} from './capabilities'
import Promise from 'promise'
import sauceConnectLauncher from 'sauce-connect-launcher'

const useLocalSauceLabs = process.env.SAUCELABS === 'true' || false
// const useBrowserStack = process.env.SAUCELABS === 'true' || false

let sauceConnectProcess

let config = {
  // Level of logging verbosity: silent | verbose | command | data | result | error
  logLevel: 'error',
  coloredLogs: true,
  screenshotPath: paths.test.errorShots,
  baseUrl: 'http://localhost:5000',
  waitforTimeout: 500000,
  updateJob: true,
  specs: [paths.test.wdioSpec],
  sync: true,
  capabilities: [{
    name: 'Chrome (local)',
    browserName: 'chrome'
  }],
  framework: 'mocha',
  reporters: ['dot'],
  mochaOpts: {
    ui: 'bdd',
    compilers: ['js:babel-core/register'],
    timeout: 100000
  }
}

const sauceLabsConfig = {
  user: process.env.SAUCE_USERNAME,
  key: process.env.SAUCE_ACCESS_KEY,
  capabilities: [ie10]
}
//
// if (useBrowserStack) {
//   config = {
//     ...config,
//     desiredCapabilities: {
//       browserName: 'chrome',
//       browser_version: '46.0',
//       os: 'Windows',
//       os_version: '10',
//       resolution: '1024x768'
//     },
//     host: 'hub.browserstack.com',
//     port: 80,
//     user: 'lewisbabbage1',
//     key: 'eumEzmmD6Cp8CRyyURuh',
//     loglevel: 'verbose'
//   }
// }

if (process.env.TRAVIS === 'true') {
  config = {
    ...config,
    ...sauceLabsConfig,
    logLevel: 'debug  '
  }
} else {
  if (useLocalSauceLabs) {
    config = {
      ...config,
      ...sauceLabsConfig,
      onPrepare: function() {
        return new Promise(function(resolve, reject) {
          sauceConnectLauncher({
            username: process.env.SAUCE_USERNAME,
            accessKey: process.env.SAUCE_ACCESS_KEY
          }, function(err, process) {
            if (err) {
              console.log(err)
              reject(err)
            } else {
              console.log('Sauce Connect is ready.')
              sauceConnectProcess = process
              resolve()
            }
          })
        }).catch(function(err) {
          console.error(err.message)
          if (sauceConnectProcess) {
            sauceConnectProcess.close()
          }
        })
      },
      onComplete: function() {
        if (typeof sauceConnectProcess !== 'undefined') {
          sauceConnectProcess.close(function() {
            console.log('Closed Sauce Connect process.')
          })
        }
      }
    }
  }
}

export default config

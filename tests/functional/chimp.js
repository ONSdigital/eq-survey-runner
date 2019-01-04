let config = {
  name: 'Survey Runner Functional Tests',
  path: 'tests/functional/spec/',
  browser: 'chrome',

  screenshotsOnError: true,
  saveScreenshotsToReport: true,

  sync: false,

  chai: true,
  mocha: true,

  webdriverio: {
    baseUrl: process.env.EQ_FUNCTIONAL_TEST_ENV || 'http://localhost:5000',
    desiredCapabilities: {
      browserName: 'chrome',
      javascriptEnabled: true,
      maxInstances: 5,
      bail: 1,
      waitForTimeout: 1000,
      waitForInterval: 500,
      chromeOptions: {
        args: [
          process.env.EQ_RUN_FUNCTIONAL_TESTS_HEADLESS ? '--headless' : '--start-maximized',
          '--window-size=1280,1080',
          '--no-sandbox',
          '--disable-gpu',
          '--disable-extensions'
        ]
      }
    }
  },

  // - - - - SELENIUM-STANDALONE
  seleniumStandaloneOptions: {
    // check for more recent versions of selenium here:
    // http://selenium-release.storage.googleapis.com/index.html
    drivers: {
      chrome: {
        // check for more recent versions of chrome driver here:
        // http://chromedriver.storage.googleapis.com/index.html
        version: '2.38',
      }
    }
  }
};

let sauceLabsConfig = {
  user: process.env.SAUCE_USER,
  key: process.env.SAUCE_KEY,
  port: 80,
  host: 'ondemand.saucelabs.com',

  webdriverio: {
    baseUrl: process.env.BASEURL
  }
};

if(process.env.SAUCE_USER) {
  config = Object.assign(config, sauceLabsConfig);
}

module.exports = config;

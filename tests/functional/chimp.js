let config = {
  name: "Survey Runner Functional Tests",
  path: "tests/functional/spec/",
  browser: "chrome",

  screenshotsOnError: true,
  saveScreenshotsToReport: true,

  sync: false,

  chai: true,
  mocha: true,
  mochaConfig: {
    // tags and grep only work when watch mode is false
    tags: '',
    grep: null,
    timeout: 50000000,
    waitForTimeout: 100000,
    waitForInterval:100000,
    reporter: 'spec',
    slow: 10000,
    useColors: true
  },

  webdriverio: {
    baseUrl: process.env.EQ_FUNCTIONAL_TEST_ENV || "http://localhost:5000",
    bail: 1,
    waitForTimeout: 100000,
    waitForInterval: 100000,
    framework: 'mocha',
    mochaOpts: {
      timeout: 1
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
  host: "ondemand.saucelabs.com",

  webdriverio: {
    baseUrl: process.env.BASEURL
  }
};

if (process.env.SAUCE_USER) {
  config = Object.assign(config, sauceLabsConfig);
}

module.exports = config;

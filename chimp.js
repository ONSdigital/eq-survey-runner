let config = {
    name: "Survey Runner Functional Tests",
    path: "tests/new_functional/spec/",
    browser: "chrome",

    // debug: true,

    // - - - - MOCHA  - - - -
    mocha: true,

    webdriverio: {
        baseUrl: "http://localhost:5000",
        desiredCapabilities: {
          browserName: "chrome",
          javascriptEnabled: true,
          maxInstances: 5,
          bail: 1,
          waitForTimeout: 1000,
          waitForInterval: 500,
          chromeOptions: {
            args: [
              "--headless",
              "--window-size=1280,1080",
              "--no-sandbox",
              "--disable-gpu"
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
          version: '2.32',
        }
      }
    }
}

let sauceLabsConfig = {
    user: process.env.SAUCE_USER,
    key: process.env.SAUCE_KEY,
    port: 80,
    host: "ondemand.saucelabs.com",

    webdriverio: {
        baseUrl: process.env.DASHVID_UI_ADDRESS
    }
}

if(process.env.SAUCE_USER) {
    console.log("Testing with Sauce Labs")
    config = Object.assign(config, sauceLabsConfig);
}

module.exports = config;

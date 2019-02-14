const cypress = require('cypress');

cypress.run({
  headed: process.env.EQ_RUN_FUNCTIONAL_TESTS_HEADLESS ? false : true,
  config: {
    baseUrl: process.env.EQ_FUNCTIONAL_TEST_ENV || "http://localhost:5000",
    viewportWidth: 1280,
    viewportHeight: 1080,
    video: false,
    integrationFolder: "tests/functional/cypress/spec/"
  }
});

module.exports = function(config) {
  var testDir = 'tests/karma'

  config.set({

    basePath: './../../',

    client: {
      mocha: {
        timeout: 4000
      }
    },

    frameworks: ['browserify', 'mocha', 'chai-sinon', 'chai'],

    files: [
      testDir + '/spec/**/*.js'
    ],

    preprocessors: {
      'tests/karma/spec/**/*.js': ['browserify'],
      '*.js': ['coverage']
    },

    plugins: [
      'karma-chrome-launcher',
      'karma-mocha-reporter',
      'karma-browserify',
      'karma-mocha',
      'karma-chai-sinon',
      'karma-chai',
      'karma-coverage'
    ],

    browserify: {
      debug: true,
      transform: ['babelify'],
      paths: ['./node_modules', './app/assets/js/']
    },

    reporters: ['mocha', 'progress', 'coverage'],

    browsers: ['ChromeHeadlessNoSandbox'],

    customLaunchers: {
      ChromeHeadlessNoSandbox: {
        base: 'ChromeHeadless',
        flags: ['--no-sandbox']
      }
    },

    coverageReporter: {
      dir : 'coverage/',
      reporters: [
        { type: 'html', subdir: 'html' },
        { type: 'lcovonly', subdir: 'lcov' },
        { type: 'cobertura', subdir: 'cobertura' }
      ]
    },


    mochaReporter: {
      output: 'full'
    },

    colors: true,
    logLevel: config.LOG_INFO
  })
}

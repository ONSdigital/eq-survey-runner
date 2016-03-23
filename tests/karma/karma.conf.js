module.exports = function(config) {

  var appDir = 'app/js'
  var testDir = 'tests/karma'

  config.set({

    basePath: './../../',

    frameworks: ['browserify', 'mocha', 'chai-sinon', 'chai-as-promised', 'chai'],

    files: [
      testDir + '/spec/**/*.js'
    ],

    preprocessors: {
      'tests/karma/spec/**/*.js': ['browserify']
    },

    plugins: [
      'karma-mocha-reporter',
      'karma-browserify',
      'karma-mocha',
      'karma-chai-sinon',
      'karma-chai-as-promised',
      'karma-chai',
      'karma-phantomjs-launcher'
    ],

    browserify: {
      debug: true,
      transform: ['babelify'],
      paths: ['./node_modules', './app/js/app/']
    },

    reporters: ['mocha'],

    browsers: ['PhantomJS'],

    coverageReporter: {
      type: 'html',
      dir: testDir + '/coverage/'
    },

    mochaReporter: {
      output: 'full'
    },

    colors: true,
    logLevel: config.LOG_DEBUG
  })
}

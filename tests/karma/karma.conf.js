module.exports = function(config) {

  var appDir = 'app/js'
  var testDir = 'tests/karma'

  config.set({

    basePath: './../../',
    frameworks: ['browserify', 'mocha', 'chai-sinon', 'chai-as-promised', 'chai'],

    files: [
      appDir + '/**/*.js',
      testDir + '/spec/**/*.js'
    ],

    preprocessors: {
      'app/js/**/*.js': ['browserify'],
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
      paths: ['./node_modules', './app/js/']
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
    logLevel: config.LOG_INFO
  })
}

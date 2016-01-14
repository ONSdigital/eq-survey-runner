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

    browserify: {
      debug: true,
      transform: ['babelify'],
      paths: ['./node_modules', './app/js/']
    },

    reporters: ['spec', 'progress'],
    browsers: ['PhantomJS'],

    // optionally, configure the reporter
    coverageReporter: {
      type: 'html',
      dir: testDir + '/coverage/'
    }
  })
}

module.exports = function(config) {
  config.set({

    basePath: './../../',
    frameworks: ['browserify', 'mocha', 'chai-sinon', 'chai-as-promised', 'chai'],

    files: [
      'app/js/**/*.js',
      'tests/karma/spec/**/*.js'
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

    reporters: ['spec'],
    browsers: ['PhantomJS']
  })
}

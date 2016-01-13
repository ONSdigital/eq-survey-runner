/**
 * Paths to project folders
 */

const paths = {
  input: 'app/**/*',
  output: 'app/static/',
  scripts: {
    input: 'app/js/*',
    output: 'app/static/js/'
  },
  styles: {
    input: 'app/sass/**/*.{scss,sass}',
    output: 'app/static/css/'
  },
  templates: {
    input: 'app/templates/**/*.html'
  },
  svgs: {
    input: 'app/img/*',
    output: 'app/static/img/'
  },
  images: {
    input: 'app/img/*',
    output: 'app/static/img/'
  },
  test: {
    input: 'app/js/**/*.js',
    karma: 'tests/karma.conf.js',
    spec: 'tests/spec/**/*.js',
    coverage: 'tests/coverage/',
    results: 'tests/results/'
  }
}

export default paths

/**
 * Paths to project folders
 */

export const srcPath = './app'
export const distPath = srcPath + '/static'

export const paths = {
  input: srcPath + '/**/*',
  output: distPath,
  scripts: {
    dir: srcPath + '/js/',
    input: srcPath + '/js/*',
    output: distPath + '/js/'
  },
  styles: {
    dir: srcPath + '/styles/',
    input: srcPath + '/styles/**/*.{scss,sass}',
    output: distPath + '/css/'
  },
  templates: {
    dir: srcPath + '/templates/',
    input: srcPath + '/templates/**/*.html'
  },
  svgs: {
    dir: srcPath + '/img/',
    input: srcPath + '/img/**/*.svg',
    output: distPath + '/img/'
  },
  images: {
    input: srcPath + '/img/**.{png,jpg,jpeg,gif,ico}',
    output: distPath + '/img/'
  },
  webfonts: {
    input: srcPath + '/webfonts/**.{svg,woff,woff2,eot,ttf}',
    output: distPath + '/webfonts/'
  },
  test: {
    input: srcPath + '/js/**/*.js',
    karma: 'tests/karma/karma.conf.js',
    spec: 'tests/karma/spec/**/*.js',
    coverage: 'tests/karma/coverage/',
    results: 'tests/karma/results/'
  }
}

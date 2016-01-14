/**
 * Paths to project folders
 */

export const srcPath = 'app'
export const distPath = srcPath + '/static'

export const paths = {
  input: srcPath + '/**/*',
  output: distPath,
  scripts: {
    input: srcPath + '/js/*',
    output: distPath + '/js/'
  },
  styles: {
    input: srcPath + '/sass/**/*.{scss,sass}',
    output: distPath + '/css/'
  },
  templates: {
    input: srcPath + '/templates/**/*.html'
  },
  svgs: {
    input: srcPath + '/img/*',
    output: distPath + '/img/'
  },
  images: {
    input: srcPath + '/img/*',
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

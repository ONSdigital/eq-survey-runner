/**
 * Paths to project folders
 */

export const appPath = './app'
export const distPath = appPath + '/static'

export const paths = {
  app: appPath,
  input: appPath + '/**/*',
  output: distPath,
  scripts: {
    dir: appPath + '/js/',
    input: appPath + '/js/**/*.js',
    output: distPath + '/js/'
  },
  styles: {
    dir: appPath + '/styles/',
    input: appPath + '/styles/**/{fixed,responsive,patterns}.scss',
    output: distPath + '/css/'
  },
  templates: {
    dir: appPath + '/templates/',
    input: appPath + '/templates/**/*.html'
  },
  svgs: {
    dir: appPath + '/img/',
    input: appPath + '/img/**/*.svg',
    output: distPath + '/img/'
  },
  images: {
    input: appPath + '/img/**.{svg,png,jpg,jpeg,gif,ico}',
    output: distPath + '/img/'
  },
  webfonts: {
    input: appPath + '/webfonts/**.{svg,woff,woff2,eot,ttf}',
    output: distPath + '/webfonts/'
  },
  test: {
    input: appPath + '/js/**/*.js',
    karmaConf: 'tests/karma/karma.conf.js',
    karmaSpec: 'tests/karma/spec/**/*.js',
    wdioConf: 'tests/wdio/wdio.conf.js',
    wdioSpec: 'tests/wdio/spec/**/*.js',
    coverage: 'tests/karma/coverage/',
    results: 'tests/karma/results/'
  }
}

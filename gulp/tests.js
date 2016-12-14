import gulp from 'gulp'
import karma from 'karma'
import path from 'path'
import gutil from 'gulp-util'
import {paths} from './paths'
import webdriver from 'gulp-webdriver'
import yargs from 'yargs'

const KarmaServer = karma.Server

export function unitTests(done, watch) {
  const server = new KarmaServer({
    configFile: path.resolve('.') + '/' + paths.test.karmaConf,
    singleRun: !watch
  }, function() {
    done()
  })

  server.on('browser_error', function(browser, err) {
    gutil.log(err)
    gutil.log('Karma Run Failed: ' + err.message)
    if (!watch) process.exit(1)
    throw err
  })

  server.on('run_complete', function(browsers, results) {
    if (results.failed) {
      if (!watch) process.exit(1)
      throw new Error('Karma: Tests Failed')
    }
    gutil.log('Karma Run Complete: No Failures')
  })

  server.start()
}

export function functionalTests(done) {
  const webdriverOpts = {}
  if (yargs.argv.spec) {
    webdriverOpts.spec = `${paths.test.wdioSpec}/${yargs.argv.spec}.spec.js`
  }
  if (yargs.argv.suite) {
    webdriverOpts.suite = yargs.argv.suite
  }
  gulp.src(paths.test.wdioConf)
    .pipe(webdriver(webdriverOpts))
    .on('error', (err) => {
      gutil.log(err)
      throw err
    })
    .once('finish', () => {
      done()
    })
}

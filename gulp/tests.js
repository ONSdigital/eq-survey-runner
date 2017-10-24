import fs from 'fs'
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
  let webdriverOpts = {}

  if (yargs.argv.spec) {
    let path = `${paths.test.wdioSpec}/${yargs.argv.spec}.spec.js`
    fs.accessSync(path)
    webdriverOpts.spec = path
  } else if (yargs.argv.suite) {
    // Run a suite
    webdriverOpts.suite = yargs.argv.suite
  }

  return _runFunctionalTests(paths.test.wdioConf, webdriverOpts, done)
}

function _runFunctionalTests(conf, options, finish) {
  gulp.src(conf)
    .pipe(webdriver(options))
    .on('error', (err) => {
      gutil.log(err)
      throw err
    })
    .once('finish', () => {
      finish()
    })
}

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

  // Execute a single spec
  if (yargs.argv.spec) {
    try {
      let path = `${paths.test.newWdioSpec}/${yargs.argv.spec}.spec.js`
      fs.accessSync(path)
      gutil.log(`Found spec in ${paths.test.newWdioSpec}`)
      webdriverOpts.spec = path

      return _runFunctionalTests(paths.test.newWdioConf, webdriverOpts, done)
    } catch (e) {
      gutil.log(`Will try to load spec from ${paths.test.wdioSpec}`)
      webdriverOpts.spec = `${paths.test.wdioSpec}/${yargs.argv.spec}.spec.js`
      return _runFunctionalTests(paths.test.wdioConf, webdriverOpts, done)
    }
  } else if (yargs.argv.suite) {
    // Run a suite

    // As suites are moved across to use the new page generator this logic will
    // need to be updated
    webdriverOpts.suite = yargs.argv.suite

    // core suite is currently split between old and new
    if (webdriverOpts.suite.includes('core')) {
      gutil.log('Running split core suite')

      return _runFunctionalTests(
        paths.test.newWdioConf,
        webdriverOpts,
        () => { _runFunctionalTests(paths.test.wdioConf, webdriverOpts, done) }
      )
    }
    return _runFunctionalTests(paths.test.wdioConf, webdriverOpts)
  } else {
    // Run *all* the tests in one go
    return _runFunctionalTests(
      paths.test.wdioConf,
      {},
      () => { _runFunctionalTests(paths.test.newWdioConf, {}, done) }
    )
  }
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

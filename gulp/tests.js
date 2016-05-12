import gulp from 'gulp'
import karma from 'karma'
import path from 'path'
import gutil from 'gulp-util'
import {paths} from './paths'
import webdriver from 'gulp-webdriver'
import selenium from 'selenium-standalone'

const KarmaServer = karma.Server

export let seleniumServer

export function startSeleniumServer(done) {
  selenium.install({logger: console.log}, () => {
    selenium.start((err, child) => {
      if (err) {
        gutil.log(err)
        return done(err)
      }
      seleniumServer = child
      done()
    })
  })
}

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
    throw err
  })

  server.on('run_complete', function(browsers, results) {
    if (results.failed) {
      throw new Error('Karma: Tests Failed')
    }
    gutil.log('Karma Run Complete: No Failures')
  })

  server.start()
}

export function functionalTests(done) {
  gulp.src(paths.test.wdioConf)
    .pipe(webdriver())
    .on('error', (err) => {
      if (typeof seleniumServer !== 'undefined') seleniumServer.kill()
      process.exit(1)
      throw err
    })
    .once('finish', () => {
      done()
      seleniumServer.kill()
    })
}

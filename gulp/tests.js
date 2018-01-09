import karma from 'karma'
import path from 'path'
import gutil from 'gulp-util'
import {paths} from './paths'

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

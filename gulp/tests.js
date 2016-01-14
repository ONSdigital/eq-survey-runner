import karma from 'karma'
import path from 'path'
import gutil from 'gulp-util'

import {
  paths
}
from './paths'
const Server = karma.Server

export function tests(done, watch) {
  const server = new Server({
    configFile: path.resolve('.') + '/' + paths.test.karma,
    singleRun: !watch
  }, function() {
    done()
  })

  server.on('browser_error', function(browser, err) {
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

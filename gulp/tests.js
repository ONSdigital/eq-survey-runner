import karma from 'karma'
import path from 'path'

import {paths} from './paths'
const Server = karma.Server

export function tests(done, watch) {
  new Server({
    configFile: path.resolve('.') + '/' + paths.test.karma,
    singleRun: watch
  }, function() {
    done()
  }).start()
}

import gulp from 'gulp'
import exec from 'gulp-exec'
import gutil from 'gulp-util'

// var exec = require('child_process').exec

const a11ym = './node_modules/the-a11y-machine/a11ym'

const a11yOptions = {
  filterCodes: 'filter-by-codes',
  exclude: 'exclude-by-codes',
  depth: 'maximum-depth',
  maxUrls: 'maximum-urls',
  output: 'output',
  report: 'report',
  standards: 'standards',
  sniffers: 'sniffers',
  filterUrls: 'filter-by-urls',
  excludeUrls: 'exclude-by-urls',
  workers: 'workers',
  user: '--http-auth-user',
  password: '--http-auth-password'
}

function gulpA11ym(url, opts, cb) {
  let args = url

  for (let prop in opts) {
    if (opts.hasOwnProperty(prop) && typeof a11yOptions[prop] !== 'undefined') {
      args += ` --${a11yOptions[prop]} ${opts[prop]}`
    }
  }

  gulp.src('')
    .pipe(exec(`${a11ym} ${args}`), {
      pipeStdout: true
    })
    .pipe(exec.reporter({
      err: true,
      stderr: true,
      stdout: true
    }))
}

export default function(done) {
  gulpA11ym('http://localhost:5000/introduction', {
    output: './tests/a11y/'
  }, done)
}

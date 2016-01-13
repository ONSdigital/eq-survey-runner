// Scripts and tests
import gulp from 'gulp'
import gutil from 'gulp-util'
import eslint from 'gulp-eslint'
import plumber from 'gulp-plumber'
// import uglify from 'gulp-uglify'
import karma from 'gulp-karma'
import exorcist from 'exorcist'
import browserify from 'browserify'
import watchify from 'watchify'
import babelify from 'babelify'
import source from 'vinyl-source-stream'

import paths from './paths'
import browserSync from './bs'

// Input file.
watchify.args.debug = true
const bundler = watchify(browserify('./app/js/app.js', watchify.args))

// Babel transform
bundler.transform(babelify.configure({
  sourceMapRelative: './app/js'
}), { presets: ['es2015'] })

// On updates recompile
bundler.on('update', bundle)

export function bundle() {
  return bundler.bundle()
    .on('error', function(err) {
      gutil.log(err.message)
      browserSync.notify('Browserify Error!')
      this.emit('end')
    })
    .pipe(exorcist('./app/static/js/bundle.js.map'))
    .pipe(source('bundle.js'))
    .pipe(gulp.dest('./app/static/js'))
    .pipe(browserSync.reload({stream: true}))
}

export function lint() {
  return gulp.src(paths.scripts.input)
    .pipe(plumber())
    .pipe(eslint())
    .pipe(eslint.format())
}

export function testScripts() {
  return gulp.src([paths.test.input].concat([paths.test.spec]))
    .pipe(plumber())
    .pipe(karma({
      configFile: paths.test.karma
    }))
    .on('error', (err) => {
      throw err
    })
}

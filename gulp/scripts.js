// Scripts and tests
import gulp from 'gulp'
import gutil from 'gulp-util'
import eslint from 'gulp-eslint'
import plumber from 'gulp-plumber'
import uglify from 'gulp-uglify'
import browserify from 'browserify'
import watchify from 'watchify'
import babelify from 'babelify'
import babel from 'gulp-babel'
import source from 'vinyl-source-stream'
import buffer from 'vinyl-buffer'
import sourcemaps from 'gulp-sourcemaps'

import {paths, srcPath, distPath} from './paths'
import browserSync from './bs'

const b = browserify(Object.assign(watchify.args, {
  entries: [`./${srcPath}/js/app/main.js`],
  debug: true
}))
.on('update', () => bundle())
.on('log', gutil.log)
.transform(babelify)

export function bundle(watch) {
  const bundler = watch ? watchify(b) : b
  bundler.bundle()
    .on('error', function(err) {
      gutil.log(err.message)
      browserSync.notify('Browserify Error!')
      this.emit('end')
    })
    .pipe(source('bundle.js'))
    .pipe(buffer())
    .pipe(uglify())
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(`./${distPath}/js`))
    .pipe(browserSync.reload({stream: true}))
}

export function copyScripts() {
  gulp.src([paths.scripts.input, `!${paths.scripts.dir}app/**/*`])
    .on('error', function(err) {
      gutil.log(err.message)
    })
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(babel())
    .pipe(plumber())
    .pipe(uglify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.scripts.output))
    .pipe(browserSync.reload({stream: true}))
}

export function lint() {
  gulp.src([paths.scripts.input, `!${paths.scripts.dir}vendor/**/*`])
    .pipe(plumber())
    .pipe(eslint())
    .pipe(eslint.format())
}

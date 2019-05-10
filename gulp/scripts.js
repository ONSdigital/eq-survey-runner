// Scripts and tests
import gulp from 'gulp'
import gutil from 'gulp-util'
import eslint from 'gulp-eslint'
import plumber from 'gulp-plumber'

import {paths} from './paths'

export function lint() {
  // Adding the tests glob to the app code glob doesn't work.
  // either the tests or app code fail to throw lint errors
  // (depending on the order they appear in the array).
  // As a work around they're split into two distinct steps
  gulp.src(['gulp/**/*.js'])
    .pipe(plumber())
    .pipe(eslint())
    .pipe(eslint.results(results => results.warningCount ? gutil.log('eslint warning') : gutil.noop()))
    .pipe(eslint.format())
    .pipe(eslint.failOnError())
    .on('error', (error) => {
      gutil.log('linting failed')
      gutil.log(error)
      process.exit(1)
    })
}

export function lintFunctionalTests() {
  gulp.src([paths.test.functional + '/**/*.js'])
    .pipe(plumber())
    .pipe(eslint())
    .pipe(eslint.results(results => results.warningCount ? gutil.log('eslint warning') : gutil.noop()))
    .pipe(eslint.format())
    .pipe(eslint.failOnError())
    .on('error', (error) => {
      gutil.log('linting failed')
      gutil.log(error)
      process.exit(1)
    })
}

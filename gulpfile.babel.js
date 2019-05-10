import gulp from 'gulp'
import gutil from 'gulp-util'
import del from 'del'
import prettify from 'gulp-jsbeautifier'
import diff from 'gulp-diff'

import { paths } from './gulp/paths'
import { lint as lintScripts, lintFunctionalTests } from './gulp/scripts'
import browserSync from './gulp/bs'

// Remove pre-existing content from output and test folders
gulp.task('clean:dist', () => {
  del.sync([paths.output], { force: true })
})

// Spin up livereload server and listen for file changes
gulp.task('listen', () => {
  browserSync.init({
    proxy: process.env.EQ_SURVEY_RUNNER_URL,
    open: false,
    port: 5075,
    ui: {
      port: 5076
    }
  })
  gulp.watch(paths.templates.input).on('change', browserSync.reload)
})

// Lint scripts
gulp.task('lint:scripts', () => {
  lintScripts()
})

gulp.task('lint:tests', () => {
  lintFunctionalTests()
})

// Compile files and generate docs when something changes
gulp.task('watch', [
  'clean:dist',
  'listen'
])

// Run unit tests
gulp.task('test', ['default', 'test:scripts'])
// Run unit tests
gulp.task('lint', ['lint:scripts', 'lint:json', 'lint:tests'])

gulp.task('lint:json', () => {
  return gulp
    .src(['./data/*/*.json'])
    .pipe(prettify({end_with_newline: true}))
    .pipe(diff())
    .pipe(
      diff.reporter({
        quiet: false,
        fail: true
      })
    )
    .on('error', err => {
      gutil.log('Linting failed try running `yarn format`')
      throw err
    })
})

gulp.task('format:json', () => {
  return gulp
    .src(['./data/*/*.json'])
    .pipe(prettify({end_with_newline: true}))
    .pipe(gulp.dest('./data/'))
})

gulp.task('format:census', () => {
  return gulp
    .src(['./data-source/*.json'])
    .pipe(prettify({end_with_newline: true}))
    .pipe(gulp.dest('./data-source/'))
})

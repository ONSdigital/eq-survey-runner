import gulp from 'gulp'
import del from 'del'
import plumber from 'gulp-plumber'

import {paths} from './gulp/paths'
import {bundle, lint} from './gulp/scripts'
import {tests} from './gulp/tests'
import {svg, images} from './gulp/images'
import styles from './gulp/styles'
import browserSync from './gulp/bs'

// Process, lint, and minify Sass files
gulp.task('build:styles', () => {
  styles()
})

// Process, lint, and minify Sass files
gulp.task('build:styles', () => {
  styles()
})

// Remove pre-existing content from output and test folders
gulp.task('clean:dist', () => {
  del.sync([
    paths.output
  ])
})

// Remove pre-existing content from text folders
gulp.task('clean:test', () => {
  del.sync([
    paths.test.coverage,
    paths.test.results
  ])
})

gulp.task('test:scripts', (done) => {
  tests(done, false)
})

// Spin up livereload server and listen for file changes
gulp.task('listen', () => {
  browserSync.init({
    proxy: 'eq-survey-runner.dev:5000',
    browser: false
  })
  gulp.watch(paths.styles.input, ['build:styles']).on('change', browserSync.reload)
  gulp.watch(paths.templates.input).on('change', browserSync.reload)
})

gulp.task('build:scripts', ['clean:dist'], () => {
  bundle()
})

gulp.task('watch:scripts', ['clean:dist'], () => {
  bundle(true)
})

gulp.task('copy:dist', function() {
  gulp.src(paths.webfonts.input)
    .pipe(plumber())
    .pipe(gulp.dest(paths.webfonts.output))
})

// Lint scripts
gulp.task('lint:scripts', () => {
  lint()
})

// Generate SVG sprites
gulp.task('build:svgs', ['clean:dist'], () => {
  svg()
})

// Copy image files into output folder
gulp.task('build:images', ['clean:dist'], () => {
  images()
})

/**
 * Task Runners
 */

// Compile files
gulp.task('compile', [
  'lint:scripts',
  'clean:dist',
  'build:scripts',
  'build:styles',
  'build:images',
  'build:svgs',
  'copy:dist'
])

/**
 * First bundle, then serve from the ./app directory
 */
gulp.task('default', [
  'compile'
])

// Compile files and generate docs when something changes
gulp.task('watch', [
  'lint:scripts',
  'clean:dist',
  'watch:scripts',
  'build:styles',
  'build:images',
  'build:svgs',
  'copy:dist',
  'listen'
])

// Run unit tests
gulp.task('test', [
  'default',
  'test:scripts'
])

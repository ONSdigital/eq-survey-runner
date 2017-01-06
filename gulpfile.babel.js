import gulp from 'gulp'
import gutil from 'gulp-util'
import del from 'del'
import yargs from 'yargs'

import {paths} from './gulp/paths'
import {copyScripts, bundle, lint as lintScripts} from './gulp/scripts'
import {unitTests, functionalTests } from './gulp/tests'
import {sprite, images} from './gulp/images'
import {styles, lint as lintStyles} from './gulp/styles'
import browserSync from './gulp/bs'
import a11ym from './gulp/a11ym'
import {fonts} from './gulp/fonts'

const getEnv = () => {
  const envs = {
    local: 'http://localhost:5000',
    preprod: 'https://preprod-surveys.eq.ons.digital'
  }
  return envs[yargs.argv.env] || envs['local']
}

gulp.task('test:a11ym', (done) => {
  a11ym(done)
})

// Process, lint, and minify Sass files
gulp.task('build:styles', () => {
  gutil.log('build:styles')
  styles()
})

// Lint scripts
gulp.task('lint:styles', () => {
  lintStyles()
})

// Remove pre-existing content from output and test folders
gulp.task('clean:dist', () => {
  del.sync([
    paths.output
  ], { force: true })
})

// Remove pre-existing content from text folders
gulp.task('clean:test', () => {
  del.sync([
    paths.test.coverage,
    paths.test.results
  ], { force: true })
})

gulp.task('test:scripts', ['test:scripts:unit', 'test:scripts:functional:sauce'])

gulp.task('test:scripts:functional', (done) => {
  process.env.BASEURL = getEnv()
  functionalTests(done)
})

gulp.task('test:scripts:functional:sauce', (done) => {
  process.env.BASEURL = getEnv()
  functionalTests(done)
})

gulp.task('test:scripts:unit', (done) => {
  unitTests(done, false)
})

gulp.task('test:scripts:unit:watch', (done) => {
  unitTests(done, true)
})

gulp.task('test:a11ym', (done) => {
  a11ym(done)
})

// Spin up livereload server and listen for file changes
gulp.task('listen', () => {
  browserSync.init({
    proxy: process.env.EQ_SURVEY_RUNNER_URL,
    open: false
  })
  gulp.watch(paths.images.input, ['build:images'])
  gulp.watch(paths.styles.input_all, ['build:styles'])
  gulp.watch([paths.scripts.input, `!${paths.scripts.dir}app/**/*`], ['copy:scripts'])
  gulp.watch(paths.templates.input).on('change', browserSync.reload)
})

gulp.task('bundle:scripts', () => {
  bundle()
})

gulp.task('copy:scripts', () => {
  copyScripts()
})

gulp.task('watch:scripts', () => {
  bundle(true)
})

// Lint scripts
gulp.task('lint:scripts', () => {
  lintScripts()
})

// Generate SVG sprites
gulp.task('build:sprite', () => {
  sprite()
})

// Copy image files into output folder
gulp.task('build:images', () => {
  images()
})

// Copy font files into output folder
gulp.task('build:fonts', () => {
  fonts()
})

/**
 * Task Runners
 */

// Compile files
gulp.task('compile', [
  'clean:dist',
  'lint:scripts',
  'lint:styles',
  'build:sprite',
  'bundle:scripts',
  'copy:scripts',
  'build:styles',
  'build:images',
  'build:fonts'
])

/**
 * First bundle, then serve from the ./app directory
 */
gulp.task('default', [
  'compile'
])

// Compile files and generate docs when something changes
gulp.task('watch', [
  'clean:dist',
  'build:sprite',
  'build:styles',
  'build:images',
  'watch:scripts',
  'build:fonts',
  'listen'
])

// Run unit tests
gulp.task('test', [
  'default',
  'test:scripts'
])
// Run unit tests
gulp.task('lint', [
  'lint:styles',
  'lint:scripts'
])

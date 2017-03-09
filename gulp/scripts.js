// Scripts and tests
import gulp from 'gulp'
import gutil from 'gulp-util'
import eslint from 'gulp-eslint'
import rename from 'gulp-rename'
import plumber from 'gulp-plumber'
import uglify from 'gulp-uglify'
import browserify from 'browserify'
import watchify from 'watchify'
import babel from 'gulp-babel'
import source from 'vinyl-source-stream'
import buffer from 'vinyl-buffer'
import sourcemaps from 'gulp-sourcemaps'

import rollupBabel from 'rollup-plugin-babel'
import nodeResolve from 'rollup-plugin-node-resolve'
import commonjs from 'rollup-plugin-commonjs'

import {paths, appPath} from './paths'
import browserSync from './bs'

let cache

const b = browserify({
  ...watchify.args,
  ...{
    entries: [`./${appPath}/js/polyfills.js`, `./${appPath}/js/app/main.js`],
    debug: true
  }
})
.on('update', () => {
  cache = bundle()
})
.on('error', gutil.log)
.on('log', gutil.log)
.transform('rollupify', {
  config: {
    cache: cache,
    entry: `./${appPath}/js/app/main.js`,
    plugins: [
      commonjs({
        include: 'node_modules/**',
        namedExports: {
          'node_modules/events/events.js': Object.keys(require('events'))
        }
      }),
      nodeResolve({
        jsnext: true,
        main: true,
        preferBuiltins: false
      }),
      rollupBabel({
        plugins: ['lodash'],
        presets: ['es2015-rollup', 'stage-2'],
        babelrc: false,
        exclude: 'node_modules/**'
      })
    ]
  }
})

export function bundle(watch) {
  const bundler = watch ? watchify(b) : b
  return bundler.bundle()
    .on('error', function(err) {
      gutil.log(err.message)
      browserSync.notify('Browserify Error!')
    })
    .pipe(source('bundle.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(gulp.dest(paths.scripts.output))
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(uglify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.scripts.output))
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
    .pipe(gulp.dest(paths.scripts.output))
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(uglify())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.scripts.output))
    .pipe(browserSync.reload({stream: true}))
}

export function lint(done) {
  return gulp.src([paths.scripts.input, `!${paths.scripts.dir}vendor/**/*`, `!${paths.scripts.dir}polyfills.js`])
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

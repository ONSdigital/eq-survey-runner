// Styles
import gulp from 'gulp'
import gutil from 'gulp-util'
import debug from 'gulp-debug'
import plumber from 'gulp-plumber'
import sass from 'gulp-sass'
import sassGlob from 'gulp-sass-glob'
import minify from 'gulp-cssnano'
import autoprefixer from 'autoprefixer'
import postcss from 'gulp-postcss'
import pxtorem from 'postcss-pxtorem'
import scss from 'postcss-scss'
import sourcemaps from 'gulp-sourcemaps'
import flatten from 'gulp-flatten'
import rename from 'gulp-rename'
import size from 'gulp-size'
import stylelint from 'stylelint'
import reporter from 'postcss-reporter'

import {paths} from './paths'
import browserSync from './bs'

export function lint() {
  gulp.src(paths.styles.input)
    .pipe(postcss([
      stylelint({}),
      reporter({ clearMessages: true })
    ], {
      syntax: scss
    }))
}

export default function styles() {
  gulp.src(paths.styles.input)
    .pipe(sourcemaps.init())
    .pipe(plumber())
    .pipe(sassGlob())
    .pipe(sass({
      errLogToConsole: true,
      outputStyle: 'expanded',
      sourceComments: false,
      includePaths: [
        './node_modules/eq-sass/',
        './node_modules/gfm.css/source/'
      ],
      onSuccess: function(msg) {
        gutil.log('Done', gutil.colors.cyan(msg))
      }
    })
    // .pipe(debug({title: 'CSS:'}))
    .on('error', function(err) {
      gutil.log(err.message.toString())
      browserSync.notify('Browserify Error!')
      this.emit('end')
    }))
    .pipe(flatten())
    .pipe(postcss([
      autoprefixer({
        browsers: ['last 1 version']
      }),
      pxtorem({
        rootValue: 18,
        propWhiteList: [],
        selectorBlackList: [],
        replace: false,
        mediaQuery: true,
        minPixelValue: 0
      }),
      reporter({ clearMessages: true })
    ]))
    .pipe(gulp.dest(paths.styles.output))
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(minify({
      calc: false,
      discardComments: {
        removeAll: true
      }
    }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.styles.output))
    .pipe(browserSync.stream({once: true}))
}

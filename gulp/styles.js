// Styles
import gulp from 'gulp'
import gutil from 'gulp-util'
import plumber from 'gulp-plumber'
import sass from 'gulp-sass'
import sassGlob from 'gulp-sass-glob'
import minify from 'gulp-cssnano'
import autoprefixer from 'autoprefixer'
import postcss from 'gulp-postcss'
import pxtorem from 'postcss-pxtorem'
import sourcemaps from 'gulp-sourcemaps'
import flatten from 'gulp-flatten'
import rename from 'gulp-rename'
import size from 'gulp-size'

import {paths} from './paths'
import browserSync from './bs'

export default function styles() {
  return gulp.src(paths.styles.input)
    .pipe(sourcemaps.init())
    .pipe(plumber())
    .pipe(sassGlob())
    .pipe(sass({
      errLogToConsole: true,
      outputStyle: 'expanded',
      sourceComments: false,
      onSuccess: function(msg) {
        gutil.log('Done', gutil.colors.cyan(msg))
      }
    }).on('error', function(err) {
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
        rootValue: 16,
        propWhiteList: [],
        selectorBlackList: [],
        replace: false,
        mediaQuery: true,
        minPixelValue: 0
      })
    ]))
    .pipe(gulp.dest(paths.styles.output))
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(minify({
      discardComments: {
        removeAll: true
      }
    }))
    .pipe(sourcemaps.write('.'))
    .pipe(size({'title': 'CSS (minified)'}))
    .pipe(gulp.dest(paths.styles.output))
    .pipe(browserSync.stream({once: true}))
}

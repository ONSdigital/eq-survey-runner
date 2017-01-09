// Styles
import gulp from 'gulp'
import gulpif from 'gulp-if'
import gutil from 'gulp-util'
import debug from 'gulp-debug'
import plumber from 'gulp-plumber'
import sass from 'gulp-sass'
import sassGlob from 'gulp-sass-glob'
import minify from 'gulp-cssnano'
import autoprefixer from 'autoprefixer'
import postcss from 'gulp-postcss'
import pixrem from 'pixrem'
import scss from 'postcss-scss'
import pseudoelements from 'postcss-pseudoelements'
import sourcemaps from 'gulp-sourcemaps'
import lazypipe from 'lazypipe'
import rename from 'gulp-rename'
import stylelint from 'stylelint'
import reporter from 'postcss-reporter'
import inlineblock from 'postcss-inline-block'

import { paths } from './paths'
import browserSync from './bs'

export function lint() {
  gulp.src(paths.styles.input)
    .pipe(postcss([
      stylelint({
        ignoreFiles: [`${paths.styles.dir}/partials/base/_sprite.scss`]
      }),
      reporter({ clearMessages: true })
    ], {
      syntax: scss
    }))
}

export function styles() {
  const minifyAssets = process.env.EQ_MINIMIZE_ASSETS === 'True'

  const minifyStyles = lazypipe()
    .pipe(rename, {
      suffix: '.min'
    })
    .pipe(minify, {
      calc: false,
      discardComments: {
        removeAll: true
      }
    })
    .pipe(gulp.dest, paths.styles.output)

  return gulp.src(paths.styles.input)
    .pipe(sourcemaps.init())
    .pipe(plumber())
    .pipe(sassGlob())
    .pipe(sass({
      errLogToConsole: true,
      outputStyle: 'expanded',
      sourceComments: false,
      includePaths: [
        paths.styles.dir
      ],
      onSuccess: function(msg) {
        gutil.log('Done', gutil.colors.cyan(msg))
      }
    })
    .on('error', function(err) {
      gutil.log(err.message.toString())
      browserSync.notify('Browserify Error!')
      this.emit('end')
    }))
    .pipe(postcss([
      autoprefixer({
        browsers: ['last 2 versions', 'Explorer >= 8', 'Android >= 4.1', 'Safari >= 7', 'iOS >= 7']
      }),
      pixrem({
        replace: false
      }),
      inlineblock(),
      pseudoelements(),
      reporter({ clearMessages: true })
    ]))
    .pipe(rename(function(path) {
      path.dirname = path.dirname.replace('themes/', '')
      return path
    }))
    .pipe(gulpif(!minifyAssets, sourcemaps.write('.')))
    .pipe(gulp.dest(paths.styles.output))
    .pipe(browserSync.reload({ stream: true }))
    .pipe(gulpif(minifyAssets, minifyStyles()))
}

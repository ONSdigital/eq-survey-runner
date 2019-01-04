// Styles
import gulp from 'gulp';
import gutil from 'gulp-util';
import plumber from 'gulp-plumber';
import sass from 'gulp-sass';
import sassGlob from 'gulp-sass-glob';
import cssnano from 'cssnano';
import autoprefixer from 'autoprefixer';
import postcss from 'gulp-postcss';
import pixrem from 'pixrem';
import pseudoelements from 'postcss-pseudoelements';
import sourcemaps from 'gulp-sourcemaps';
import rename from 'gulp-rename';
import gulpStylelint from 'gulp-stylelint';
import reporter from 'postcss-reporter';
import inlineblock from 'postcss-inline-block';

import { paths } from './paths';
import browserSync from './bs';

export function lint() {
  gulp.src([paths.styles.input_all]).pipe(
    gulpStylelint({
      reporters: [{ formatter: 'string', console: true }]
    }).on('error', error => {
      gutil.log('linting failed');
      gutil.log(error);
      process.exit(1);
    })
  );
}

export function styles() {
  const minifyAssets =
    process.env.EQ_MINIMIZE_ASSETS === undefined ||
    process.env.EQ_MINIMIZE_ASSETS === 'True';

  let postCssPlugins = [
    autoprefixer({
      browsers: [
        'last 2 versions',
        'Explorer >= 8',
        'Android >= 4.1',
        'Safari >= 7',
        'iOS >= 7'
      ]
    }),
    pixrem({
      replace: false
    }),
    inlineblock(),
    pseudoelements(),
    reporter({ clearMessages: true })
  ];

  if (minifyAssets) {
    postCssPlugins.push(
      cssnano({
        calc: false,
        discardComments: {
          removeAll: true
        }
      })
    );
  }

  let assets = gulp
    .src(paths.styles.input)
    .pipe(sourcemaps.init())
    .pipe(plumber())
    .pipe(sassGlob())
    .pipe(
      sass({
        errLogToConsole: true,
        outputStyle: 'expanded',
        sourceComments: false,
        includePaths: [paths.styles.dir],
        onSuccess: function(msg) {
          gutil.log('Done', gutil.colors.cyan(msg));
        }
      }).on('error', function(err) {
        gutil.log(err.message.toString());
        browserSync.notify('Browserify Error!');
        this.emit('end');
      })
    )
    .pipe(postcss(postCssPlugins))
    .pipe(
      rename(function(path) {
        path.dirname = path.dirname.replace('themes/', '');
        return path;
      })
    );

  if (minifyAssets) {
    assets = assets.pipe(rename({ suffix: '.min' })).pipe(sourcemaps.write('.'));
  }

  return assets
    .pipe(gulp.dest(paths.styles.output))
    .pipe(browserSync.reload({ stream: true }));
}

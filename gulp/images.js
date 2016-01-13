import gulp from 'gulp'
import plumber from 'gulp-plumber'
import tap from 'gulp-tap'
import size from 'gulp-size'
import svgmin from 'gulp-svgmin'
import svgstore from 'gulp-svgstore'
import {paths} from './paths'

// Generate SVG sprites
export function svg() {
  return gulp.src(paths.svgs.input)
    .pipe(plumber())
    .pipe(tap((file, t) => {
      if (file.isDirectory()) {
        let name = file.relative + '.svg'
        gulp.src(file.path + '/*.svg')
          .pipe(svgmin())
          .pipe(svgstore({
            fileName: name,
            prefix: 'icon-',
            inlineSvg: true
          }))
          .pipe(gulp.dest(paths.svgs.output))
      }
    }))
    .pipe(svgmin())
    .pipe(size({'title': 'SVG'}))
    .pipe(gulp.dest(paths.svgs.output))
}

export function images() {
  return gulp.src(paths.images.input)
    .pipe(plumber())
    .pipe(gulp.dest(paths.images.output))
}

import gulp from 'gulp'
import {paths} from './paths'

export function favicons() {
  gulp.src(paths.favicons.input)
    .pipe(gulp.dest(paths.favicons.output))
}

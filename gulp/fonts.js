import gulp from 'gulp'
import {paths} from './paths'

export function fonts() {
  gulp.src(paths.fonts.input)
    .pipe(gulp.dest(paths.fonts.output))
}

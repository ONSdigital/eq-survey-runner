import gulp from 'gulp'
import gutil from 'gulp-util'
import plumber from 'gulp-plumber'
import tap from 'gulp-tap'
import size from 'gulp-size'
import svgmin from 'gulp-svgmin'
import svgstore from 'gulp-svgstore'
import svgSprite from 'gulp-svg-sprite'
import {paths} from './paths'
import browserSync from './bs'

export function svg() {
  gulp.src(paths.svgs.input)
    .pipe(svgSprite({
      shape: {
        dimension: {
          maxWidth: 32,
          maxHeight: 32
        },
        spacing: {
          padding: 10
        }
      },
      mode: {
        inline: true,
        symbol: {
          example: {
            template: `${paths.svgs.dir}/icons/tmpl.html`,
            dest: `../../../../${paths.templates.dir}/patterns/components/icons.html`
          },
          render: {
            scss: {
              dest: `../../../../${paths.styles.dir}/base/_sprite.scss`
            }
          }
        }
      }
    }))
    .on('error', function(err) {
      gutil.log(err.message.toString())
      browserSync.notify('Browserify Error!')
      this.emit('end')
    })
    .pipe(gulp.dest(paths.svgs.output))
}

// // Generate SVG sprites
// export function svg() {
//   gulp.src(paths.svgs.input)
//     .pipe(plumber())
//     .pipe(tap((file, t) => {
//       if (file.isDirectory()) {
//         let name = file.relative + '.svg'
//         gulp.src(file.path + '/**/*.svg')
//           .pipe(svgmin())
//           .pipe(svgstore({
//             fileName: name,
//             prefix: 'icon-',
//             inlineSvg: true
//           }))
//           .pipe(gulp.dest(paths.svgs.output))
//       }
//     }))
//     .pipe(svgmin())
//     .pipe(size({'title': 'SVG'}))
//     .pipe(gulp.dest(paths.svgs.output))
// }

export function images() {
  gulp.src(paths.images.input)
    .pipe(plumber())
    .pipe(gulp.dest(paths.images.output))
}

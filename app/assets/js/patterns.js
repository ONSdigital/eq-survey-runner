/* global Prism:true */

(() => {
  Prism.plugins.NormalizeWhitespace.setDefaults({
    'remove-trailing': true,
    'remove-indent': true,
    'left-trim': true,
    'right-trim': true,
    'indent': 0,
    'remove-initial-line-feed': false,
    'tabs-to-spaces': 1
  })

  let $nav, $header
  const scrollHandler = () => {
    if (window.scrollY > $header[0].scrollHeight) {
      $nav.addClass('is-fixed')
    } else {
      $nav.removeClass('is-fixed')
    }
  }

  $(window).on('scroll', (e) => {
    window.requestAnimationFrame(scrollHandler)
  })

  $(() => {
    $nav = $('#ptn-nav')
    $header = $('#ptn-header')
  })
})()

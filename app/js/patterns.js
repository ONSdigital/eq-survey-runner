/*global Prism:true */
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

  let nav, header, highlight
  const scrollHandler = () => {
    if (window.scrollY > header.scrollHeight) {
      nav.classList.add('is-fixed')
    } else {
      nav.classList.remove('is-fixed')
    }
  }

  $(window).on('scroll', (e) => {
    window.requestAnimationFrame(scrollHandler)
  })

  $(() => {
    nav = document.querySelector('#ptn-nav')
    header = document.querySelector('#ptn-header')
    highlight = document.querySelectorAll('.highlight')
    $(highlight).each((index, el) => {
      var element =
        `<div class=="ptn-code is-closed">
          ${el}
        </div>`
      console.log(element)
    })
  })
})()

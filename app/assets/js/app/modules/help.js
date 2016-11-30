import domready from './domready'

domready(() => {
  const btn = document.querySelector('.js-help-btn')
  const help = document.querySelector('.js-help-body')
  const classClosed = 'is-closed'

  let openedByClick = false

  if (help === null || btn === null) {
    return false
  }

  help.addEventListener('focus', e => {
    help.classList.remove(classClosed)
  }, true)

  help.addEventListener('blur', e => {
    if (!openedByClick) {
      help.classList.add(classClosed)
    }
  }, true)

  btn.classList.remove('u-hidden')
  btn.addEventListener('click', e => {
    e.preventDefault()
    openedByClick = !openedByClick
    help.classList.toggle(classClosed)
  })
})

import domready from './domready'

domready(() => {
  Array.from(document.getElementsByClassName('btn-print'))
    .forEach(el => el.addEventListener('click', () => window.print()))
})

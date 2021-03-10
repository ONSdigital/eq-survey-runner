import domready from './domready'

domready(() => {
  Array.from(document.getElementsByClassName('btn-download-pdf')).forEach((el) => el.addEventListener('click', () => {
    alert('hi')
    fetch('/download_submission')
  }))
})

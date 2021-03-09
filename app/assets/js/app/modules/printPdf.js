import domready from './domready'

const downloadPdf = async() => {
  await fetch('/download_submission')
}

domready(() => {
  document.getElementById('btn-download-pdf').addEventListener('click', downloadPdf)
})

import domready from './domready'

export default function initPrintlistener() {
  let printed = false
  const onafterPrinting = () => {
    if (!printed) {
      window.dataLayer.push({ 'event': 'onAfterPrint', 'currentURL': location.pathname })
      printed = true
    }
  }
  if (window.matchMedia) {
    let mql = window.matchMedia('print')
    mql.addEventListener("change", (e) => {
      if (!e.matches) {
        onafterPrinting()
      }
    })
  }
  window.onafterprint = onafterPrinting
}

domready(initPrintlistener)

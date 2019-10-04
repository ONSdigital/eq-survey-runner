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
    let mediaQueryList = window.matchMedia('print')
    mediaQueryList.addListener(function(mql) {
      if (mql.matches) {
        onafterPrinting()
      }
    })
  }
  window.onafterprint = onafterPrinting
}

domready(initPrintlistener)

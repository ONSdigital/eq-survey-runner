let callback
const EVENT_DOM_READY = 'DOMContentLoaded'

const onReady = (e) => {
  callback.call()
  document.removeEventListener(EVENT_DOM_READY, onReady)
}

export default function ready(fn) {
  if (document.readyState !== 'loading') {
    fn()
  } else {
    callback = fn
    document.addEventListener(EVENT_DOM_READY, onReady)
  }
}

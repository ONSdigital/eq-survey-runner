const eventReady = 'DOMContentLoaded'

let callbacks = []

const onReady = () => {
  callbacks.forEach(fn => fn.call())
  document.removeEventListener(eventReady, onReady)
}

export default function ready(fn) {
  callbacks.push(fn)
  if (document.readyState !== 'loading') {
    onReady.call()
  } else {
    document.addEventListener(eventReady, onReady)
  }
}

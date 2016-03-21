const inputSelector = '.js-charlimit-input'
const msgSelector = '.js-charlimit-msg'

export function applyCharLimit(limitField, limitNum) {
  if (limitField.value.length > limitNum) {
    limitField.value = limitField.value.substring(0, limitNum)
  }

  return limitField.value.length
}

export function updateDOM(el, length, maxLength) {
  el.innerHTML = 0 - (maxLength - length)
}

export function imposeCharLimit(el, maxLength) {
  const msgEl = el.parentElement.querySelector(msgSelector)

  updateDOM(msgEl, maxLength, 0)

  el.addEventListener('input', (e) => {
    let currLength = applyCharLimit(el, maxLength)
    updateDOM(msgEl, maxLength, currLength)
  })
}

export default function() {
  const nodeList = document.querySelectorAll(inputSelector)

  Array.prototype.slice.call(nodeList).forEach(function(el) {
    const maxLength = el.getAttribute('data-maxlength')
    if (typeof maxLength !== 'undefined') {
      imposeCharLimit(el, maxLength)
    }
  })

  return nodeList
}

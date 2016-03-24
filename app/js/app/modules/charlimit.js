export const inputClass = 'js-charlimit-input'
export const msgClass = 'js-charlimit-msg'
export const maxLengthAttr = 'data-maxlength'

export function applyCharLimit(limitValue, limit) {
  if (limitValue.length > limit) {
    limitValue = limitValue.substring(0, limit)
  }

  return limitValue
}

export function updateMsg(el, length, maxLength) {
  el.innerHTML = 0 - (maxLength - length)
}

export function imposeCharLimit(el, maxLength) {
  const msgEl = el.parentElement.querySelector(`.${msgClass}`)

  updateMsg(msgEl, maxLength, 0)

  el.addEventListener('input', (e) => {
    el.value = applyCharLimit(el.value, maxLength)
    updateMsg(msgEl, maxLength, el.value.length)
  })
}

export default function() {
  const nodeList = document.querySelectorAll(`.${inputClass}`)

  Array.prototype.slice.call(nodeList).forEach(function(el) {
    const maxLength = el.getAttribute(maxLengthAttr)
    if (typeof maxLength !== 'undefined') {
      imposeCharLimit(el, maxLength)
    }
  })

  return nodeList
}

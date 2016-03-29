import domready from './domready'
import _ from 'lodash'

export const inputClass = 'js-charlimit-input'
export const msgClass = 'js-charlimit-msg'
export const maxLengthAttr = 'data-maxlength'

export default function() {
  return charLimit()
}

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

  updateMsg(msgEl, maxLength, el.value.length)

  el.addEventListener('input', (e) => {
    el.value = applyCharLimit(el.value, maxLength)
    updateMsg(msgEl, maxLength, el.value.length)
  })
}

export function charLimit() {
  const nodeList = document.getElementsByClassName(inputClass)

  _.forEach(nodeList, (el) => {
    const maxLength = el.getAttribute(maxLengthAttr)
    if (typeof maxLength !== 'undefined') {
      imposeCharLimit(el, maxLength)
    }
  })

  return nodeList
}

domready(charLimit)

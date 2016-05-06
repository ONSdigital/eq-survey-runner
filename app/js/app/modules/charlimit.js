import domready from './domready'
import forEach from 'lodash/forEach'

export const inputClass = 'js-charlimit-input'
export const msgClass = 'js-charlimit-msg'
export const msgLabel = 'js-charlimit-label'
export const attrMaxLength = 'data-maxlength'
export const attrRemainingMsg = 'data-remaining-msg'

export default function charLimit() {
  const nodeList = document.getElementsByClassName(inputClass)

  forEach(nodeList, (el) => {
    const maxLength = parseInt(el.getAttribute(attrMaxLength), 10)
    if (typeof maxLength !== 'undefined') {
      imposeCharLimit(el, maxLength)
    }
  })

  return nodeList
}

export function applyCharLimit(inputTextValue, limit) {
  if (inputTextValue.length > limit) {
    return inputTextValue.substring(0, limit)
  } else {
    return inputTextValue
  }
}

export function updateMsg(el, length, maxLength) {
  el.innerHTML = 0 - (maxLength - length)
}

export function imposeCharLimit(el, maxLength) {
  const elMsg = el.parentElement.querySelector(`.${msgClass}`)
  const elLabel = el.parentElement.getElementsByClassName(msgLabel)[0]

  elLabel.innerHTML = elLabel.getAttribute(attrRemainingMsg)

  updateMsg(elMsg, maxLength, el.value.length)

  el.addEventListener('input', (e) => {
    el.value = applyCharLimit(el.value, maxLength)
    updateMsg(elMsg, maxLength, el.value.length)
  })
}

domready(charLimit)

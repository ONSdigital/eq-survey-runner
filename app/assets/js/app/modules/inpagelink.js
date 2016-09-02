import forEach from 'lodash/forEach'
import domready from './domready'

export const classDetails = 'js-inpagelink'
export const classTrigger = 'js-inpagelink-trigger'

export const attrInputId = 'data-inputid'

export default function() {
  return inPageLink()
}

export function inPageLink() {
  const nodeList = document.getElementsByClassName(classDetails)
  forEach(nodeList, applyInPageLink)
  return nodeList
}

export function applyInPageLink(elDetails) {
  const elTrigger = elDetails.getElementsByClassName(classTrigger)[0]
  const elId = elDetails.getAttribute(attrInputId)
  elTrigger.addEventListener('click', (e) => {
    e.preventDefault()
    focusOnInput(elId)
  })

  return {elDetails, elTrigger, elId}
}

function focusOnInput(elId) {
  const elIdInput = document.getElementById(elId).getElementsByClassName('input')[0]
  elIdInput.focus()
  return elId
}

domready(inPageLink)

import forEach from 'lodash/forEach'
import domready from './domready'

export const classDetails = 'js-details'
export const classTrigger = 'js-details-trigger'
export const classBody = 'js-details-body'
export const classLabel = 'js-details-label'
export const classExpandedState = 'is-expanded'

export const attrShowLbl = 'data-show-label'
export const attrHideLbl = 'data-hide-label'
export const attrAriaExpanaded = 'aria-expanded'
export const attrAriaHidden = 'aria-hidden'
export const attrTabIndex = 'tabindex'

export default function() {
  return detailsToggle()
}

export function detailsToggle() {
  const nodeList = document.getElementsByClassName(classDetails)
  forEach(nodeList, applyDetailsToggle)
  return nodeList
}

export function applyDetailsToggle(elDetails) {
  const elTrigger = elDetails.getElementsByClassName(classTrigger)[0]
  const elBody = elDetails.getElementsByClassName(classBody)[0]
  const elLabel = elDetails.getElementsByClassName(classLabel)[0]
  let toggled = false

  elTrigger.addEventListener('click', (e) => {
    e.preventDefault()
    toggled = toggle(toggled, elDetails, elTrigger, elBody, elLabel)
    return false
  })

  return {elDetails, elTrigger, elBody}
}

export function open(elDetails, elBody, elLabel, elTrigger) {
  elDetails.classList.add(classExpandedState)
  elLabel.innerHTML = elDetails.getAttribute(attrHideLbl)
  elTrigger.setAttribute(attrAriaExpanaded, true)
  elBody.setAttribute(attrAriaHidden, false)
}

export function close(elDetails, elBody, elLabel, elTrigger) {
  elDetails.classList.remove(classExpandedState)
  elLabel.innerHTML = elDetails.getAttribute(attrShowLbl)
  elTrigger.setAttribute(attrAriaExpanaded, false)
  elBody.setAttribute(attrAriaHidden, true)
}

export function toggle(toggled, elDetails, elTrigger, elBody, elLabel) {
  !toggled ? open(elDetails, elBody, elLabel, elTrigger) : close(elDetails, elBody, elLabel, elTrigger)
  return !toggled
}

domready(detailsToggle)

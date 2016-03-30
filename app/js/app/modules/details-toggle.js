import _ from 'lodash'
import domready from './domready'

export const classDetails = 'js-details'
export const classTrigger = 'js-details-trigger'
export const classMain = 'js-details-main'
export const classLabel = 'js-details-label'
export const classExpandedState = 'is-expanded'

export const attrShowLbl = 'data-show-label'
export const attrHideLbl = 'data-hide-label'
export const attrAriaExpanaded = 'aria-expanded'
export const attrAriaHidden = 'aria-hidden'

export default function() {
  return detailsToggle()
}

export function detailsToggle() {
  const nodeList = document.getElementsByClassName(classDetails)

  _.forEach(nodeList, applyDetailsToggle)

  return nodeList
}

export function applyDetailsToggle(elDetails) {
  const elTrigger = elDetails.parentElement.getElementsByClassName(classTrigger)[0]
  const elMain = elDetails.getElementsByClassName(classMain)[0]
  const elLabel = elDetails.getElementsByClassName(classLabel)[0]
  let toggled = false

  elTrigger.addEventListener('click', (e) => {
    e.preventDefault()
    toggled = toggle(toggled, elDetails, elTrigger, elMain, elLabel)
    return false
  })
}

export function toggle(toggled, elDetails, elTrigger, elMain, elLabel) {
  elTrigger.setAttribute(attrAriaExpanaded, toggled)
  elMain.setAttribute(attrAriaHidden, !toggled)

  if (!toggled) {
    elDetails.classList.add(classExpandedState)
    elMain.focus()
    elLabel.innerHTML = elDetails.getAttribute(attrHideLbl)
  } else {
    elDetails.classList.remove(classExpandedState)
    elMain.blur()
    elLabel.innerHTML = elDetails.getAttribute(attrShowLbl)
  }

  return !toggled
}

domready(detailsToggle)

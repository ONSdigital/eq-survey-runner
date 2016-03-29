import _ from 'lodash'
import domready from './domready'

const classDetails = 'js-details'
const classTrigger = 'js-details-trigger'
const classMain = 'js-details-main'
const classLabel = 'js-details-label'
const classExpandedState = 'is-expanded'

const attrShowLbl = 'data-show-label'
const attrHideLbl = 'data-hide-label'
const attrAriaExpanaded = 'aria-expanded'
const attrAriaHidden = 'aria-hidden'

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

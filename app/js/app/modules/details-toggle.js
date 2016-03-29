import _ from 'lodash'
import domready from './domready'

export const detailsClass = 'js-details'
export const triggerClass = 'js-details-trigger'
export const mainClass = 'js-details-main'
export const expandedStateClass = 'is-expanded'

export default function() {
  return detailsToggle()
}

export function detailsToggle() {
  const nodeList = document.getElementsByClassName(detailsClass)

  _.forEach(nodeList, (el) => {
    applyDetailsToggle(el)
  })

  return nodeList
}

export function applyDetailsToggle(el) {
  const triggerEl = el.parentElement.getElementsByClassName(triggerClass)[0]

  triggerEl.addEventListener('click', (e) => {
    const mainElement = el.getElementsByClassName(mainClass)[0]
    e.preventDefault()

    triggerEl.setAttribute('aria-expanded', 'true')
    el.classList.add('is-expanded')

    mainElement.focus()
    mainElement.setAttribute('aria-hidden', 'false')

    return false
  })
}

domready(detailsToggle)

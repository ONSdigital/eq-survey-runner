import {forEach} from 'lodash'
import domready from './domready'

export const hasJs = 'has-js'
export const classAccordion = 'js-accordion'
export const classAccordionItem = 'js-accordion-item'
export const classAccordionTrigger = 'js-accordion-trigger'
export const classAccordionBody = 'js-accordion-body'
export const classClosed = 'is-closed'

export const attrHidden = 'aria-hidden'

const accordionItems = []

export default function accordion() {
  return forEach(document.getElementsByClassName(classAccordion), applyAccordion)
}

export function applyAccordion(elAccordion) {
  return forEach(elAccordion.getElementsByClassName(classAccordionItem), applyAccordionItem)
}

export function applyAccordionItem(elAccordionItem) {
  elAccordionItem.classList.add(hasJs)
  closeAccordion(elAccordionItem)

  accordionItems.push(elAccordionItem)

  forEach(elAccordionItem.getElementsByClassName(classAccordionTrigger), elAccordionTrigger => {
    elAccordionTrigger.removeAttribute('tabindex')
    elAccordionTrigger.addEventListener('click', e => {
      e.preventDefault()
      toggleAccordion(elAccordionItem)
    })
  })
}

function closeAllExcept(elAccordion) {
  accordionItems
    .filter(item => item !== elAccordion)
    .map(item => closeAccordion(item))
}

function closeAccordion(elAccordion) {
  elAccordion.getElementsByClassName(classAccordionBody)[0].setAttribute(attrHidden, true)
  elAccordion.classList.add(classClosed)
}

function openAccordion(elAccordion) {
  elAccordion.getElementsByClassName(classAccordionBody)[0].setAttribute(attrHidden, false)
  elAccordion.classList.remove(classClosed)
}

function toggleAccordion(elAccordion) {
  closeAllExcept(elAccordion)
  if (elAccordion.classList.contains(classClosed)) {
    openAccordion(elAccordion)
  } else {
    closeAccordion(elAccordion)
  }
}

domready(accordion)

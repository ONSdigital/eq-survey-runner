import {forEach} from 'lodash'
import domready from './domready'
import {trackEvent} from './analytics'

export const classHasJs = 'has-js'
export const classAccordion = 'js-accordion'
export const classAccordionContent = 'js-accordion-content'
export const classAccordionTitle = 'js-accordion-title'
export const classAccordionBody = 'js-accordion-body'
export const classExpanded = 'is-expanded'
export const classPreview = 'js-accordion-preview'
export const classClose = 'js-accordion-close'
export const classAccordionOpenAll = 'js-accordion-open-all'
export const classAccordionCloseAll = 'js-accordion-close-all'
export const classHidden = 'u-hidden'

export const attrHidden = 'aria-hidden'
export const attrExpanded = 'aria-expanded'
export const attrMultiselectable = 'aria-multiselectable'
export const attrControls = 'aria-controls'
export const attrSelected = 'aria-selected'

class Accordion {
  constructor(trackEvent) {
    this.trackEvent = trackEvent
    this.openItems = 0
  }

  registerDom(rootEl) {
    rootEl.classList.add(classHasJs)

    const content = rootEl.getElementsByClassName(classAccordionContent)[0]
    content.setAttribute('role', 'tablist')
    content.setAttribute(attrMultiselectable, 'true')

    this.titles = forEach(
      rootEl.getElementsByClassName(classAccordionTitle),
      (el, index) => { this.registerTitle(el, index) }
    )

    this.bodys = forEach(
      rootEl.getElementsByClassName(classAccordionBody),
      (el, index) => { this.registerBody(el, index) }
    )

    this.openAllTriggers = forEach(
      rootEl.getElementsByClassName(classAccordionOpenAll),
      el => { this.registerOpenAll(el) }
    )

    this.closeAllTriggers = forEach(
      rootEl.getElementsByClassName(classAccordionCloseAll),
      el => { this.registerCloseAll(el) }
    )

    this.updateOpenCloseTriggerDisplay()
  }

  registerTitle(element, index) {
    // Better screen reader interaction
    element.setAttribute('id', 'accordion-title-' + index)
    element.setAttribute('role', 'tab')
    element.setAttribute(attrControls, 'accordion-body-' + index)
    element.setAttribute(attrExpanded, 'false')
    element.setAttribute(attrSelected, 'false')

    // Content of this container is keyboard navigable so
    // ensure that the this container isn't
    element.setAttribute('tabindex', '-1')

    if (element.classList.contains(classExpanded)) {
      element.setAttribute(attrExpanded, 'true')
      this.openItems += 1

      // No-JS envs don't need a close prompt
      this.show(element.getElementsByClassName(classClose)[0])
    } else {
      // No-JS envs don't need a preview prompt
      this.show(element.getElementsByClassName(classPreview)[0])
    }

    element.addEventListener('click', e => {
      e.preventDefault()
      this.toggle(element)
    })

    element.addEventListener('keydown', e => {
      this.keyboardInteraction(element, e)
    })
  }

  registerBody(element, index) {
    // Better screen reader interaction
    element.setAttribute('id', 'accordion-body-' + index)
    element.setAttribute('role', 'tabpanel')
    element.setAttribute('aria-labelledby', 'accordion-title-' + index)
    element.setAttribute(attrHidden, 'true')
  }

  registerOpenAll(openAllEl) {
    openAllEl.addEventListener('click', e => {
      e.preventDefault()

      forEach(this.titles, el => { this.open(el) })

      this.updateOpenCloseTriggerDisplay()
    })
  }

  registerCloseAll(closeAllEl) {
    closeAllEl.addEventListener('click', e => {
      e.preventDefault()

      forEach(this.titles, el => { this.close(el) })

      this.updateOpenCloseTriggerDisplay()
    })
  }

  updateOpenCloseTriggerDisplay() {
    if (this.openItems / this.titles.length < 1) {
      forEach(this.closeAllTriggers, trigger => this.hide(trigger))
      forEach(this.openAllTriggers, trigger => this.show(trigger))
    } else {
      forEach(this.openAllTriggers, trigger => this.hide(trigger))
      forEach(this.closeAllTriggers, trigger => this.show(trigger))
    }
  }

  toggle(element) {
    let action = ''

    if (element.getAttribute(attrExpanded) === 'true') {
      this.close(element)
      action = 'Close question'
    } else {
      this.open(element)
      action = 'Open question'
    }

    this.updateOpenCloseTriggerDisplay()

    this.publishEvent(action, element.getAttribute('data-js-accordion-event-label'))
  }

  open(titleEl) {
    if (titleEl.getAttribute(attrExpanded) === 'true') return

    const bodyEl = titleEl.nextElementSibling

    titleEl.classList.add(classExpanded)
    titleEl.setAttribute(attrExpanded, true)
    titleEl.setAttribute(attrSelected, true)

    this.hide(titleEl.getElementsByClassName(classPreview)[0])
    this.show(titleEl.getElementsByClassName(classClose)[0])

    bodyEl.classList.add(classExpanded)
    bodyEl.setAttribute(attrHidden, false)

    this.openItems += 1
  }

  close(titleEl) {
    if (titleEl.getAttribute(attrExpanded) === 'false') return

    const bodyEl = titleEl.nextElementSibling

    titleEl.classList.remove(classExpanded)
    titleEl.setAttribute(attrExpanded, false)
    titleEl.setAttribute(attrSelected, false)

    this.show(titleEl.getElementsByClassName(classPreview)[0])
    this.hide(titleEl.getElementsByClassName(classClose)[0])

    bodyEl.classList.remove(classExpanded)
    bodyEl.setAttribute(attrHidden, true)

    this.openItems -= 1
  }

  hide(element) {
    element.classList.add(classHidden)
  }

  show(element) {
    element.classList.remove(classHidden)
  }

  publishEvent(action, label) {
    this.trackEvent('send', {
      hitType: 'event',
      eventCategory: 'Preview Survey',
      eventAction: action,
      eventLabel: label
    })
  }

  keyboardInteraction(elem, e) {
    const keyCode = e.which
    switch (keyCode) {
      // Enter/Space
      case 13:
      case 32:
        e.preventDefault()
        e.stopPropagation()

        // Show answer content
        this.toggle(elem)
        break
    }
  }
}

export default function accordion(eventTracker = trackEvent) {
  const elAccordion = document.getElementsByClassName(classAccordion)

  forEach(elAccordion, element => new Accordion(eventTracker).registerDom(element))
}

domready(accordion)

import domready from './domready'
import getTransitionEndEvent from '../helpers/transitionend'

const transitionEndEvent = getTransitionEndEvent()

export const classExpanded = 'is-expanded'
export const classCollapsed = 'is-collapsed'
export const classHidden = 'u-hidden'

export const classFeedbackThanks = '.js-feedback-thanks'
export const classFeedbackCancel = '.js-feedback-cancel'
export const classInlineForm = '.js-feedback-inline'
export const classFeedbackOpen = '.js-feedback-open'
export const classCallToAction = '.js-feedback-action'
export const classMessage = '.js-feedback-message'
export const className = '.js-feedback-name'
export const classEmail = '.js-feedback-email'
export const classSubmit = '.js-feedback-submit'

export const attrHidden = 'aria-hidden'

export const feedbackEndPoint = '/feedback'

class Feedback {
  constructor(form, callToAction, thanks, cancel, open) {
    // This module relies on browsers having implemented
    // the FormData Interface
    // (https://developer.mozilla.org/en-US/docs/Web/API/FormData)
    // < IE10 don't have it so they get the No-JS fallback
    if (window.FormData) {
      this.form = form
      this.registerForm(this.form)

      this.callToAction = callToAction
      this.open = open
      this.registerOpen(this.open)

      this.thanks = thanks

      this.cancel = cancel
      this.registerCancel(this.cancel)
    }
  }

  registerForm(element) {
    element.setAttribute(attrHidden, 'true')

    const elSubmit = element.querySelector(classSubmit)
    this.registerSubmit(elSubmit)
  }

  registerSubmit(element) {
    element.addEventListener('click', e => {
      e.preventDefault()

      this.sendFeedback()
      this.collapse(this.form)
      this.hide(this.callToAction)
      this.show(this.thanks)
    })
  }

  registerOpen(element) {
    element.addEventListener('click', e => {
      e.preventDefault()

      this.expand(this.form)
    })
  }

  registerCancel(element) {
    element.addEventListener('click', e => {
      e.preventDefault()

      this.collapse(this.form)
    })
  }

  sendFeedback() {
    const form = this.form.querySelector('form')
    const formData = new FormData(form)
    formData.append('redirect', 'false')

    fetch(feedbackEndPoint, {
      method: 'POST',
      body: formData,
      credentials: 'include'
    })

    // NB: clearing textarea like this does not update remaining chars
    this.form.querySelector(classMessage).value = ''
  }

  expand(element) {
    element.classList.remove(classCollapsed)
    window.setTimeout(function() {
      element.classList.add(classExpanded)
    }, 20)
    element.setAttribute(attrHidden, false)
  }

  collapse(element) {
    element.addEventListener(transitionEndEvent, this.onTransitionCollapseEnd.bind(this), { once: true })
    element.classList.remove(classExpanded)
    element.setAttribute(attrHidden, true)
  }

  onTransitionCollapseEnd(event) {
    event.target.classList.add(classCollapsed)
  }

  hide(element) {
    element.classList.add(classHidden)
  }

  show(element) {
    element.classList.remove(classHidden)
  }
}

export default function feedback() {
  const elFeedback = document.querySelector(classInlineForm)
  const elCallToAction = document.querySelector(classCallToAction)
  const elOpen = document.querySelector(classFeedbackOpen)
  const elThanks = document.querySelector(classFeedbackThanks)
  const elCancel = document.querySelector(classFeedbackCancel)

  return new Feedback(elFeedback, elCallToAction, elThanks, elCancel, elOpen)
}

domready(feedback)

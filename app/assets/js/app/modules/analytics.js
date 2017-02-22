import {forEach} from 'lodash'
import domready from './domready'

export default function initAnalytics() {
  let trackEvent = (event, data) => {
    console.log(`[Analytics disabled] Event: ${event}`)
    console.log(data)
  }

  if (typeof window.ga !== 'undefined') {
    trackEvent = (evt, data) => window.ga(evt, data)
  } else {
    console.log('Analytics disabled')
  }

  const errors = document.querySelectorAll('[data-error=true]')
  const guidances = document.querySelectorAll('[data-guidance]')
  const previousLinks = document.querySelectorAll('.js-previous-link')
  const helpAndSupport = document.querySelector('.js-help-and-support')

  forEach(errors, error => {
    const errorMsg = error.getAttribute('data-error-msg')
    const elementId = error.getAttribute('data-error-id')
    const errorData = {
      hitType: 'event',
      eventCategory: 'Errors',
      eventAction: errorMsg,
      eventLabel: elementId
    }
    trackEvent('send', errorData)
  })

  forEach(guidances, guidance => {
    const trigger = guidance.querySelector('[data-guidance-trigger]')
    const questionLabel = document.title
    const questionId = guidance.getAttribute('data-guidance')

    const onClickGuidance = e => {
      trigger.removeEventListener('click', onClickGuidance)
      const triggerData = {
        hitType: 'event',
        eventCategory: 'Guidance',
        eventAction: questionLabel,
        eventLabel: questionId
      }
      trackEvent('send', triggerData)
    }

    if (trigger) {
      trigger.addEventListener('click', onClickGuidance)
    }
  })

  forEach(previousLinks, previousLink => {
    const onClickPrev = e => {
      const triggerData = {
        hitType: 'event',
        eventCategory: 'Navigation',
        eventAction: 'previous-link'
      }
      trackEvent('send', triggerData)
    }
    previousLink.addEventListener('click', onClickPrev)
  })

  const onClickHelp = e => {
    helpAndSupport.removeEventListener('click', onClickHelp)
    const triggerData = {
      hitType: 'event',
      eventCategory: 'Navigation',
      eventAction: 'help-and-support'
    }
    trackEvent('send', triggerData)
  }
  if (helpAndSupport) {
    helpAndSupport.addEventListener('click', onClickHelp)
  }
}

domready(initAnalytics)

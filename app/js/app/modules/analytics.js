import forEach from 'lodash/forEach'
import domready from './domready'

export default function initAnalytics() {
  const errors = document.querySelectorAll('[data-error=true]')
  forEach(errors, (error) => {
    const errorMsg = error.getAttribute('data-error-msg')
    const errorValue = error.getAttribute('data-error-value')
    const elementId = error.getAttribute('data-error-id')
    const errorData = {
      hitType: 'event',
      eventCategory: 'Errors',
      eventAction: `${errorMsg} (${errorValue})`,
      eventLabel: elementId
    }
    console.log(errorData)
    ga('send', errorData)
  })
}

domready(initAnalytics)

import 'ie9-oninput-polyfill'
import domready from './domready'
import {trackEvent} from './analytics'

const inputClassLimitExceeded = 'input--limit-reached'
const remainingClassLimitExceeded = 'input__limit--reached'
const classCharactersRemaining = 'input__limit'
const classLimitedInput = 'js-charlimit-input'

domready(() => {
  const remainingCharElements = document.querySelectorAll(`.${classCharactersRemaining}`)
  const fieldSet = document.querySelector('body')

  const onAnswerChanged = (e) => {
    const element = e.target

    if (element.type !== 'textarea') return
    updateAvailableChars(element)
  }

  const updateAvailableChars = (element) => {
    // data-maxlength is used to store the original value of maxlength
    // before we mess with it when newlines are added to the input
    const limit = element.getAttribute('data-maxlength')
    let maxLength = limit - countNewlines(element.value)
    element.setAttribute('maxlength', maxLength)

    let count = maxLength - element.value.length
    // If the user pastes something in the count could be
    // negative (because we're double counting newlines), so...
    if (count < 0) {
      element.value = element.value.slice(0, maxLength)
      count = 0
    }

    const remainingCharElement = findRemainingCharElement(element.id)

    if (remainingCharElement) {
      remainingCharElement.firstElementChild.innerText = count
      highlightWhenLimitReached(remainingCharElement, remainingClassLimitExceeded, count)
      highlightWhenLimitReached(element, inputClassLimitExceeded, count)

      if (count < 1) {
        trackEvent('send', {
          hitType: 'event',
          eventCategory: 'Error',
          eventAction: 'Textarea limit reached',
          eventLabel: `Limit of ${limit} reached/exceeded`
        })
      }
    }
  }

  const findRemainingCharElement = (inputId) => {
    // We assume that the character count for an input is
    // prefixed with the input elements id
    for (let i = 0; i < remainingCharElements.length; i++) {
      if (remainingCharElements[i].id.indexOf(inputId) === 0) {
        return remainingCharElements[i]
      }
    }

    return false
  }

  const initialise = () => {
    const limitedInputs = document.querySelectorAll(`.${classLimitedInput}`)

    for (let i = 0; i < limitedInputs.length; i++) {
      let input = limitedInputs[i]

      // We change the value of maxlength if there are \n's so store
      // the original value so that the calculations are correct when
      // \n's are deleted
      input.setAttribute('data-maxlength', input.getAttribute('maxlength'))
      updateAvailableChars(input)
    }
  }

  const highlightWhenLimitReached = (element, cssClass, count) => {
    if (count < 1) {
      element.classList.add(cssClass)
      return
    }

    element.classList.remove(cssClass)
  }

  const countNewlines = (aString) => {
    return (aString.match(/\n/g) || []).length
  }

  // Make sure all the character counts are correct on page load
  fieldSet.addEventListener('input', onAnswerChanged)
  initialise()
})

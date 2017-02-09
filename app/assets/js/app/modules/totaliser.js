import domready from './domready'
import getTransitionEndEvent from '../helpers/transitionend'

const transitionendEvent = getTransitionEndEvent()

domready(() => {
  const breakdownFields = document.querySelectorAll('input:not(.js-totaliser-input-calculated)')
  const totalField = document.querySelector('.js-totaliser-input-calculated')
  const fieldSet = document.querySelector('.js-question-fieldset')

  const onAnswerChanged = (e) => {
    if (e.target === totalField) {
      return
    }

    let newTotal = 0

    for (let i = 0; i < breakdownFields.length; i++) {
      let percentage = breakdownFields[i].value

      let value = parseInt(percentage)
      if (isNaN(value)) {
        continue
      } else if (value > 0) {
        newTotal += value
      }
    }

    updateTotal(newTotal)
  }

  const highlight = () => {
    addTransitionedEventListener()
    totalField.classList.add('input--has-error')
  }

  const removeHighlight = () => {
    addTransitionedEventListener()
    totalField.classList.remove('input--has-error')
  }

  const addTransitionedEventListener = () => {
    if (transitionendEvent) {
      totalField.addEventListener(transitionendEvent, onTransitionHighlightEnd, true)
    } else {
      window.setTimeout(onTransitionHighlightEnd, 500)
    }
  }

  const onTransitionHighlightEnd = (e) => {
    totalField.removeEventListener(transitionendEvent, onTransitionHighlightEnd)
  }

  const updateTotal = (value) => {
    totalField.value = value
    if (value === 100) {
      // good
      removeHighlight()
    } else {
      // bad
      highlight()
    }
  }

  if (totalField) {
    fieldSet.addEventListener('change', onAnswerChanged)
    totalField.setAttribute('readonly', 'readonly')
    let initialValue = parseInt(totalField.value)
    if (!isNaN(initialValue)) {
      updateTotal(initialValue)
    }
  }
})

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TermTimeLocationPage extends MultipleChoiceWithOtherPage {

  clickAtThisAddress() {
    browser.element('[id="term-time-location-answer-1"]').click()
    return this
  }

  clickAtAnotherAddress() {
    browser.element('[id="term-time-location-answer-2"]').click()
    return this
  }

  setTermTimeLocationAnswer(value) {
    browser.setValue('[name="term-time-location-answer"]', value)
    return this
  }

  getTermTimeLocationAnswer(value) {
    return browser.element('[name="term-time-location-answer"]').getValue()
  }

}

export default new TermTimeLocationPage()

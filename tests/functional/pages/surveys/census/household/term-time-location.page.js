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

}

export default new TermTimeLocationPage()

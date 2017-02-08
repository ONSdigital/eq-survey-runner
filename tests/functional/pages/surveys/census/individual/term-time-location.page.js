// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TermTimeLocationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('term-time-location')
  }

  clickTermTimeLocationAnswerHereAtThisAddress() {
    browser.element('[id="term-time-location-answer-0"]').click()
    return this
  }

  clickTermTimeLocationAnswerAtAnotherAddress() {
    browser.element('[id="term-time-location-answer-1"]').click()
    return this
  }

}

export default new TermTimeLocationPage()

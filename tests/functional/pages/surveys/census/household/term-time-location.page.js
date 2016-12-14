// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.774341 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TermTimeLocationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('term-time-location')
  }

  clickTermTimeLocationAnswerHereAtThisAddress() {
    browser.element('[id="term-time-location-answer-1"]').click()
    return this
  }

  clickTermTimeLocationAnswerAtAnotherAddress() {
    browser.element('[id="term-time-location-answer-2"]').click()
    return this
  }

}

export default new TermTimeLocationPage()

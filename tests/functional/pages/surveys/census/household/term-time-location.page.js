// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.863435 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TermTimeLocationPage extends MultipleChoiceWithOtherPage {

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

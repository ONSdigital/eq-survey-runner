// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.842452 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class DetailsCorrectPage extends MultipleChoiceWithOtherPage {

  clickDetailsCorrectAnswerYesThisIsMyFullName() {
    browser.element('[id="details-correct-answer-1"]').click()
    return this
  }

  clickDetailsCorrectAnswerNoINeedToChangeMyName() {
    browser.element('[id="details-correct-answer-2"]').click()
    return this
  }

}

export default new DetailsCorrectPage()

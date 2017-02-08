// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class DetailsCorrectPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('details-correct')
  }

  clickDetailsCorrectAnswerYesThisIsMyFullName() {
    browser.element('[id="details-correct-answer-0"]').click()
    return this
  }

  clickDetailsCorrectAnswerNoINeedToChangeMyName() {
    browser.element('[id="details-correct-answer-1"]').click()
    return this
  }

}

export default new DetailsCorrectPage()

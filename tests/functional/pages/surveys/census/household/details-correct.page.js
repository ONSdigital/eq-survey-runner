// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.749011 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class DetailsCorrectPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('details-correct')
  }

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

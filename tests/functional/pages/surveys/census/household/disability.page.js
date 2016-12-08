// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.829919 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class DisabilityPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('disability')
  }

  clickDisabilityAnswerYesLimitedALot() {
    browser.element('[id="disability-answer-1"]').click()
    return this
  }

  clickDisabilityAnswerYesLimitedALittle() {
    browser.element('[id="disability-answer-2"]').click()
    return this
  }

  clickDisabilityAnswerNo() {
    browser.element('[id="disability-answer-3"]').click()
    return this
  }

}

export default new DisabilityPage()

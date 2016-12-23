// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InternalInvestmentRDPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('internal-investment-r-d')
  }

  clickInternalInvestmentRDAnswerYes() {
    browser.element('[id="internal-investment-r-d-answer-0"]').click()
    return this
  }

  clickInternalInvestmentRDAnswerNo() {
    browser.element('[id="internal-investment-r-d-answer-1"]').click()
    return this
  }

}

export default new InternalInvestmentRDPage()

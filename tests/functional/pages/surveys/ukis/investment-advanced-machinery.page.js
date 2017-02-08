// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InvestmentAdvancedMachineryPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('investment-advanced-machinery')
  }

  clickInvestmentAdvancedMachineryAnswerYes() {
    browser.element('[id="investment-advanced-machinery-answer-0"]').click()
    return this
  }

  clickInvestmentAdvancedMachineryAnswerNo() {
    browser.element('[id="investment-advanced-machinery-answer-1"]').click()
    return this
  }

}

export default new InvestmentAdvancedMachineryPage()

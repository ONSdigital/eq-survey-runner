// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InvestmentTrainingInnovativePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('investment-training-innovative')
  }

  clickInvestmentTrainingInnovativeAnswerYes() {
    browser.element('[id="investment-training-innovative-answer-0"]').click()
    return this
  }

  clickInvestmentTrainingInnovativeAnswerNo() {
    browser.element('[id="investment-training-innovative-answer-1"]').click()
    return this
  }

}

export default new InvestmentTrainingInnovativePage()

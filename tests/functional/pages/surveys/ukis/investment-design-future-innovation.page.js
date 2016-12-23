// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InvestmentDesignFutureInnovationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('investment-design-future-innovation')
  }

  clickInvestmentDesignFutureInnovationAnswerYes() {
    browser.element('[id="investment-design-future-innovation-answer-0"]').click()
    return this
  }

  clickInvestmentDesignFutureInnovationAnswerNo() {
    browser.element('[id="investment-design-future-innovation-answer-1"]').click()
    return this
  }

}

export default new InvestmentDesignFutureInnovationPage()

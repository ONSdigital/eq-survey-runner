// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InvestmentIntroductionInnovationsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('investment-introduction-innovations')
  }

  clickInvestmentIntroductionInnovationsAnswerYes() {
    browser.element('[id="investment-introduction-innovations-answer-0"]').click()
    return this
  }

  clickInvestmentIntroductionInnovationsAnswerNo() {
    browser.element('[id="investment-introduction-innovations-answer-1"]').click()
    return this
  }

}

export default new InvestmentIntroductionInnovationsPage()

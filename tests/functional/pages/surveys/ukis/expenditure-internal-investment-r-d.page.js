// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class ExpenditureInternalInvestmentRDPage extends QuestionPage {

  constructor() {
    super('expenditure-internal-investment-r-d')
  }

  setExpenditureInternalInvestmentRDAnswer(value) {
    browser.setValue('[name="expenditure-internal-investment-r-d-answer"]', value)
    return this
  }

  getExpenditureInternalInvestmentRDAnswer(value) {
    return browser.element('[name="expenditure-internal-investment-r-d-answer"]').getValue()
  }

}

export default new ExpenditureInternalInvestmentRDPage()

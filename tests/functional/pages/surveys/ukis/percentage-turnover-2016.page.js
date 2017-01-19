// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class PercentageTurnover2016Page extends QuestionPage {

  constructor() {
    super('percentage-turnover-2016')
  }

  setPercentageTurnover2016MarketNewAnswer(value) {
    browser.setValue('[name="percentage-turnover-2016-market-new-answer"]', value)
    return this
  }

  getPercentageTurnover2016MarketNewAnswer(value) {
    return browser.element('[name="percentage-turnover-2016-market-new-answer"]').getValue()
  }

  setPercentageTurnover2016BusinessNewAnswer(value) {
    browser.setValue('[name="percentage-turnover-2016-business-new-answer"]', value)
    return this
  }

  getPercentageTurnover2016BusinessNewAnswer(value) {
    return browser.element('[name="percentage-turnover-2016-business-new-answer"]').getValue()
  }

  setPercentageTurnover2016ImprovementAnswer(value) {
    browser.setValue('[name="percentage-turnover-2016-improvement-answer"]', value)
    return this
  }

  getPercentageTurnover2016ImprovementAnswer(value) {
    return browser.element('[name="percentage-turnover-2016-improvement-answer"]').getValue()
  }

  setPercentageTurnover2016ModifiedAnswer(value) {
    browser.setValue('[name="percentage-turnover-2016-modified-answer"]', value)
    return this
  }

  getPercentageTurnover2016ModifiedAnswer(value) {
    return browser.element('[name="percentage-turnover-2016-modified-answer"]').getValue()
  }

  setPercentageTurnover2016TotalAnswer(value) {
    browser.setValue('[name="percentage-turnover-2016-total-answer"]', value)
    return this
  }

  getPercentageTurnover2016TotalAnswer(value) {
    return browser.element('[name="percentage-turnover-2016-total-answer"]').getValue()
  }

}

export default new PercentageTurnover2016Page()

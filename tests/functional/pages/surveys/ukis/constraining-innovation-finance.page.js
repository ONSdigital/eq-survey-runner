// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class ConstrainingInnovationFinancePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('constraining-innovation-finance')
  }

  clickConstrainingInnovationFinanceAnswerHigh() {
    browser.element('[id="constraining-innovation-finance-answer-0"]').click()
    return this
  }

  clickConstrainingInnovationFinanceAnswerMedium() {
    browser.element('[id="constraining-innovation-finance-answer-1"]').click()
    return this
  }

  clickConstrainingInnovationFinanceAnswerLow() {
    browser.element('[id="constraining-innovation-finance-answer-2"]').click()
    return this
  }

  clickConstrainingInnovationFinanceAnswerNotImportant() {
    browser.element('[id="constraining-innovation-finance-answer-3"]').click()
    return this
  }

}

export default new ConstrainingInnovationFinancePage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class ExpenditureDesign2016Page extends QuestionPage {

  constructor() {
    super('expenditure-design-2016')
  }

  setExpenditureDesign2016Answer(value) {
    browser.setValue('[name="expenditure-design-2016-answer"]', value)
    return this
  }

  getExpenditureDesign2016Answer(value) {
    return browser.element('[name="expenditure-design-2016-answer"]').getValue()
  }

}

export default new ExpenditureDesign2016Page()

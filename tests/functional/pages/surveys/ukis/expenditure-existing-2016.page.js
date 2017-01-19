// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class ExpenditureExisting2016Page extends QuestionPage {

  constructor() {
    super('expenditure-existing-2016')
  }

  setExpenditureExisting2016Answer(value) {
    browser.setValue('[name="expenditure-existing-2016-answer"]', value)
    return this
  }

  getExpenditureExisting2016Answer(value) {
    return browser.element('[name="expenditure-existing-2016-answer"]').getValue()
  }

}

export default new ExpenditureExisting2016Page()

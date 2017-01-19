// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class ExpenditureTrainingInnovative2016Page extends QuestionPage {

  constructor() {
    super('expenditure-training-innovative-2016')
  }

  setExpenditureTrainingInnovative2016Answer(value) {
    browser.setValue('[name="expenditure-training-innovative-2016-answer"]', value)
    return this
  }

  getExpenditureTrainingInnovative2016Answer(value) {
    return browser.element('[name="expenditure-training-innovative-2016-answer"]').getValue()
  }

}

export default new ExpenditureTrainingInnovative2016Page()

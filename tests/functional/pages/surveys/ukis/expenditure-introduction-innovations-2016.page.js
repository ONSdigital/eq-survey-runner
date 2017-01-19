// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class ExpenditureIntroductionInnovations2016Page extends QuestionPage {

  constructor() {
    super('expenditure-introduction-innovations-2016')
  }

  setExpenditureIntroductionInnovations2016Answer(value) {
    browser.setValue('[name="expenditure-introduction-innovations-2016-answer"]', value)
    return this
  }

  getExpenditureIntroductionInnovations2016Answer(value) {
    return browser.element('[name="expenditure-introduction-innovations-2016-answer"]').getValue()
  }

}

export default new ExpenditureIntroductionInnovations2016Page()

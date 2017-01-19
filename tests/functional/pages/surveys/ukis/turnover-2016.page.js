// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class Turnover2016Page extends QuestionPage {

  constructor() {
    super('turnover-2016')
  }

  setTurnover2016Answer(value) {
    browser.setValue('[name="turnover-2016-answer"]', value)
    return this
  }

  getTurnover2016Answer(value) {
    return browser.element('[name="turnover-2016-answer"]').getValue()
  }

}

export default new Turnover2016Page()

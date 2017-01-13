// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class Turnover2014Page extends QuestionPage {

  constructor() {
    super('turnover-2014')
  }

  setTurnover2014Answer(value) {
    browser.setValue('[name="turnover-2014-answer"]', value)
    return this
  }

  getTurnover2014Answer(value) {
    return browser.element('[name="turnover-2014-answer"]').getValue()
  }

}

export default new Turnover2014Page()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.727330 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class OvernightVisitorsPage extends QuestionPage {

  constructor() {
    super('overnight-visitors')
  }

  setOvernightVisitorsAnswer(value) {
    browser.setValue('[name="overnight-visitors-answer"]', value)
    return this
  }

  getOvernightVisitorsAnswer(value) {
    return browser.element('[name="overnight-visitors-answer"]').getValue()
  }

}

export default new OvernightVisitorsPage()

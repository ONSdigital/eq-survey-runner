// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.825191 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class OvernightVisitorsPage extends QuestionPage {

  setOvernightVisitorsAnswer(value) {
    browser.setValue('[name="overnight-visitors-answer"]', value)
    return this
  }

  getOvernightVisitorsAnswer(value) {
    return browser.element('[name="overnight-visitors-answer"]').getValue()
  }

}

export default new OvernightVisitorsPage()

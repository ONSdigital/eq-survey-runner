// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.910148 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class OtherPassportsPage extends QuestionPage {

  setOtherPassportsAnswer(value) {
    browser.setValue('[name="other-passports-answer"]', value)
    return this
  }

  getOtherPassportsAnswer(value) {
    return browser.element('[name="other-passports-answer"]').getValue()
  }

}

export default new OtherPassportsPage()

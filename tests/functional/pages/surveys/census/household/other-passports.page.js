// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.827786 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class OtherPassportsPage extends QuestionPage {

  constructor() {
    super('other-passports')
  }

  setOtherPassportsAnswer(value) {
    browser.setValue('[name="other-passports-answer"]', value)
    return this
  }

  getOtherPassportsAnswer(value) {
    return browser.element('[name="other-passports-answer"]').getValue()
  }

}

export default new OtherPassportsPage()

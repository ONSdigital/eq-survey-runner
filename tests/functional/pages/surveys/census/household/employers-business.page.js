// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.865119 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class EmployersBusinessPage extends QuestionPage {

  constructor() {
    super('employers-business')
  }

  setEmployersBusinessAnswer(value) {
    browser.setValue('[name="employers-business-answer"]', value)
    return this
  }

  getEmployersBusinessAnswer(value) {
    return browser.element('[name="employers-business-answer"]').getValue()
  }

}

export default new EmployersBusinessPage()

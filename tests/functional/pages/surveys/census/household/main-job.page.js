// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.860026 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MainJobPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('main-job')
  }

  clickMainJobAnswerAnEmployee() {
    browser.element('[id="main-job-answer-1"]').click()
    return this
  }

  clickMainJobAnswerSelfEmployedOrFreelanceWithoutEmployees() {
    browser.element('[id="main-job-answer-2"]').click()
    return this
  }

  clickMainJobAnswerSelfEmployedWithEmployees() {
    browser.element('[id="main-job-answer-3"]').click()
    return this
  }

}

export default new MainJobPage()

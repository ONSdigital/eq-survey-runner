// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MainJobPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('main-job')
  }

  clickMainJobAnswerAnEmployee() {
    browser.element('[id="main-job-answer-0"]').click()
    return this
  }

  clickMainJobAnswerSelfEmployedOrFreelanceWithoutEmployees() {
    browser.element('[id="main-job-answer-1"]').click()
    return this
  }

  clickMainJobAnswerSelfEmployedWithEmployees() {
    browser.element('[id="main-job-answer-2"]').click()
    return this
  }

}

export default new MainJobPage()

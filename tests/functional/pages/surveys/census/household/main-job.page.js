// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.935194 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MainJobPage extends MultipleChoiceWithOtherPage {

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

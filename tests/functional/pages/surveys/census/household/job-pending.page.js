// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.850055 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class JobPendingPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('job-pending')
  }

  clickJobPendingAnswerYes() {
    browser.element('[id="job-pending-answer-1"]').click()
    return this
  }

  clickJobPendingAnswerNo() {
    browser.element('[id="job-pending-answer-2"]').click()
    return this
  }

}

export default new JobPendingPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.840980 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class JobseekerPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('jobseeker')
  }

  clickJobseekerAnswerYes() {
    browser.element('[id="jobseeker-answer-1"]').click()
    return this
  }

  clickJobseekerAnswerNo() {
    browser.element('[id="jobseeker-answer-2"]').click()
    return this
  }

}

export default new JobseekerPage()

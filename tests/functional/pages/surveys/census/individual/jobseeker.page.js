// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class JobseekerPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('jobseeker')
  }

  clickJobseekerAnswerYes() {
    browser.element('[id="jobseeker-answer-0"]').click()
    return this
  }

  clickJobseekerAnswerNo() {
    browser.element('[id="jobseeker-answer-1"]').click()
    return this
  }

}

export default new JobseekerPage()

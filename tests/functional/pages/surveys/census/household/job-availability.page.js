// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.845756 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class JobAvailabilityPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('job-availability')
  }

  clickJobAvailabilityAnswerYes() {
    browser.element('[id="job-availability-answer-1"]').click()
    return this
  }

  clickJobAvailabilityAnswerNo() {
    browser.element('[id="job-availability-answer-2"]').click()
    return this
  }

}

export default new JobAvailabilityPage()

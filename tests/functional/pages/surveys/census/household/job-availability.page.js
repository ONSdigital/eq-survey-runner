// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.925396 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class JobAvailabilityPage extends MultipleChoiceWithOtherPage {

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

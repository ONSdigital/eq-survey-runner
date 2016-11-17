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

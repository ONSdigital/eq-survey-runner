import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class JobAvailabilityPage extends MultipleChoiceWithOtherPage {

  clickYes() {
    browser.element('[id="job-availability-answer-1"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="job-availability-answer-2"]').click()
    return this
  }

}

export default new JobAvailabilityPage()

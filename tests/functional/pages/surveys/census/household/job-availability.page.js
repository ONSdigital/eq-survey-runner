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

  setJobAvailabilityAnswer(value) {
    browser.setValue('[name="job-availability-answer"]', value)
    return this
  }

  getJobAvailabilityAnswer(value) {
    return browser.element('[name="job-availability-answer"]').getValue()
  }

}

export default new JobAvailabilityPage()

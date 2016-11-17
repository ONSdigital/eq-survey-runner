import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class JobPendingPage extends MultipleChoiceWithOtherPage {

  clickYes() {
    browser.element('[id="job-pending-answer-1"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="job-pending-answer-2"]').click()
    return this
  }

  setJobPendingAnswer(value) {
    browser.setValue('[name="job-pending-answer"]', value)
    return this
  }

  getJobPendingAnswer(value) {
    return browser.element('[name="job-pending-answer"]').getValue()
  }

}

export default new JobPendingPage()

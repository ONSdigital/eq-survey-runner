import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class JobseekerPage extends MultipleChoiceWithOtherPage {

  clickYes() {
    browser.element('[id="jobseeker-answer-1"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="jobseeker-answer-2"]').click()
    return this
  }

  setJobseekerAnswer(value) {
    browser.setValue('[name="jobseeker-answer"]', value)
    return this
  }

  getJobseekerAnswer(value) {
    return browser.element('[name="jobseeker-answer"]').getValue()
  }

}

export default new JobseekerPage()

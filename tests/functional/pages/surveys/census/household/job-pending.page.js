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

}

export default new JobPendingPage()

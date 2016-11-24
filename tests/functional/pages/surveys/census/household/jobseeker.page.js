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

}

export default new JobseekerPage()

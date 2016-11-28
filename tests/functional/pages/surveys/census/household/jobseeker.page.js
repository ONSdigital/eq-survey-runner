import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class JobseekerPage extends MultipleChoiceWithOtherPage {

  clickJobseekerAnswerYes() {
    browser.element('[id="jobseeker-answer-1"]').click()
    return this
  }

  clickJobseekerAnswerNo() {
    browser.element('[id="jobseeker-answer-2"]').click()
    return this
  }

}

export default new JobseekerPage()

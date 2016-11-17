import QuestionPage from '../../question.page'

class JobTitlePage extends QuestionPage {

  setJobTitleAnswer(value) {
    browser.setValue('[name="job-title-answer"]', value)
    return this
  }

  getJobTitleAnswer(value) {
    return browser.element('[name="job-title-answer"]').getValue()
  }

}

export default new JobTitlePage()

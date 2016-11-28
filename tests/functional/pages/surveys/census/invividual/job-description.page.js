import QuestionPage from '../../question.page'

class JobDescriptionPage extends QuestionPage {

  setJobDescriptionAnswer(value) {
    browser.setValue('[name="job-description-answer"]', value)
    return this
  }

  getJobDescriptionAnswer(value) {
    return browser.element('[name="job-description-answer"]').getValue()
  }

}

export default new JobDescriptionPage()

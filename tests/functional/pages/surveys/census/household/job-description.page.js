// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.863537 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class JobDescriptionPage extends QuestionPage {

  constructor() {
    super('job-description')
  }

  setJobDescriptionAnswer(value) {
    browser.setValue('[name="job-description-answer"]', value)
    return this
  }

  getJobDescriptionAnswer(value) {
    return browser.element('[name="job-description-answer"]').getValue()
  }

}

export default new JobDescriptionPage()

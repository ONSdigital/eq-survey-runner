// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.862160 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class JobTitlePage extends QuestionPage {

  constructor() {
    super('job-title')
  }

  setJobTitleAnswer(value) {
    browser.setValue('[name="job-title-answer"]', value)
    return this
  }

  getJobTitleAnswer(value) {
    return browser.element('[name="job-title-answer"]').getValue()
  }

}

export default new JobTitlePage()

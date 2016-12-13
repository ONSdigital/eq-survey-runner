// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.937858 - DO NOT EDIT!!! <<<

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

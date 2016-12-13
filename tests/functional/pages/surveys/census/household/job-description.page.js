// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.940406 - DO NOT EDIT!!! <<<

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

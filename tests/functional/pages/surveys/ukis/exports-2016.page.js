// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class Exports2016Page extends QuestionPage {

  constructor() {
    super('exports-2016')
  }

  setExports2016Answer(value) {
    browser.setValue('[name="exports-2016-answer"]', value)
    return this
  }

  getExports2016Answer(value) {
    return browser.element('[name="exports-2016-answer"]').getValue()
  }

}

export default new Exports2016Page()

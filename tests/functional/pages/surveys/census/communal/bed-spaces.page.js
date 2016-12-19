// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class BedSpacesPage extends QuestionPage {

  constructor() {
    super('bed-spaces')
  }

  setBedSpacesAnswer(value) {
    browser.setValue('[name="bed-spaces-answer"]', value)
    return this
  }

  getBedSpacesAnswer(value) {
    return browser.element('[name="bed-spaces-answer"]').getValue()
  }

}

export default new BedSpacesPage()

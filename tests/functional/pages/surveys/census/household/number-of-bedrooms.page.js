// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class NumberOfBedroomsPage extends QuestionPage {

  constructor() {
    super('number-of-bedrooms')
  }

  setNumberOfBedroomsAnswer(value) {
    browser.setValue('[name="number-of-bedrooms-answer"]', value)
    return this
  }

  getNumberOfBedroomsAnswer(value) {
    return browser.element('[name="number-of-bedrooms-answer"]').getValue()
  }

}

export default new NumberOfBedroomsPage()

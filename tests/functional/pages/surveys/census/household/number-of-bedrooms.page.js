// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.834300 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class NumberOfBedroomsPage extends QuestionPage {

  setNumberOfBedroomsAnswer(value) {
    browser.setValue('[name="number-of-bedrooms-answer"]', value)
    return this
  }

  getNumberOfBedroomsAnswer(value) {
    return browser.element('[name="number-of-bedrooms-answer"]').getValue()
  }

}

export default new NumberOfBedroomsPage()

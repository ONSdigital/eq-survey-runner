// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.743155 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class NumberOfVehiclesPage extends QuestionPage {

  constructor() {
    super('number-of-vehicles')
  }

  setNumberOfVehiclesAnswer(value) {
    browser.setValue('[name="number-of-vehicles-answer"]', value)
    return this
  }

  getNumberOfVehiclesAnswer(value) {
    return browser.element('[name="number-of-vehicles-answer"]').getValue()
  }

}

export default new NumberOfVehiclesPage()

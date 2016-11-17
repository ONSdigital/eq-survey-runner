import QuestionPage from '../../question.page'

class NumberOfVehiclesPage extends QuestionPage {

  setNumberOfVehiclesAnswer(value) {
    browser.setValue('[name="number-of-vehicles-answer"]', value)
    return this
  }

  getNumberOfVehiclesAnswer(value) {
    return browser.element('[name="number-of-vehicles-answer"]').getValue()
  }

}

export default new NumberOfVehiclesPage()

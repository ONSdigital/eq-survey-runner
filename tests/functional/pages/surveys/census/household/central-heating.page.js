import QuestionPage from '../../question.page'

class CentralHeatingPage extends QuestionPage {

  clickGas() {
    browser.element('[id="central-heating-answer-1"]').click()
    return this
  }

  clickElectricIncludingStorageHeaters() {
    browser.element('[id="central-heating-answer-2"]').click()
    return this
  }

  clickOil() {
    browser.element('[id="central-heating-answer-3"]').click()
    return this
  }

  clickSolidFuelForExampleWoodCoal() {
    browser.element('[id="central-heating-answer-4"]').click()
    return this
  }

  clickOtherCentralHeating() {
    browser.element('[id="central-heating-answer-5"]').click()
    return this
  }

  clickNoCentralHeating() {
    browser.element('[id="central-heating-answer-6"]').click()
    return this
  }

  setCentralHeatingAnswer(value) {
    browser.setValue('[name="central-heating-answer"]', value)
    return this
  }

  getCentralHeatingAnswer(value) {
    return browser.element('[name="central-heating-answer"]').getValue()
  }

}

export default new CentralHeatingPage()

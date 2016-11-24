import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CentralHeatingPage extends MultipleChoiceWithOtherPage {

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

}

export default new CentralHeatingPage()

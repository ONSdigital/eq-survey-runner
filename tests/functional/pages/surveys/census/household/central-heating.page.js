// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.737785 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CentralHeatingPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('central-heating')
  }

  clickCentralHeatingAnswerNoCentralHeating() {
    browser.element('[id="central-heating-answer-1"]').click()
    return this
  }

  clickCentralHeatingAnswerGas() {
    browser.element('[id="central-heating-answer-2"]').click()
    return this
  }

  clickCentralHeatingAnswerElectricIncludingStorageHeaters() {
    browser.element('[id="central-heating-answer-3"]').click()
    return this
  }

  clickCentralHeatingAnswerOil() {
    browser.element('[id="central-heating-answer-4"]').click()
    return this
  }

  clickCentralHeatingAnswerSolidFuelForExampleWoodCoal() {
    browser.element('[id="central-heating-answer-5"]').click()
    return this
  }

  clickCentralHeatingAnswerOtherCentralHeating() {
    browser.element('[id="central-heating-answer-6"]').click()
    return this
  }

}

export default new CentralHeatingPage()

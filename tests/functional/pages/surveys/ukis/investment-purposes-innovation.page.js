// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InvestmentPurposesInnovationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('investment-purposes-innovation')
  }

  clickInvestmentPurposesInnovationAnswerAdvancedMachineryAndEquipment() {
    browser.element('[id="investment-purposes-innovation-answer-0"]').click()
    return this
  }

  clickInvestmentPurposesInnovationAnswerComputerHardware() {
    browser.element('[id="investment-purposes-innovation-answer-1"]').click()
    return this
  }

  clickInvestmentPurposesInnovationAnswerComputerSoftware() {
    browser.element('[id="investment-purposes-innovation-answer-2"]').click()
    return this
  }

}

export default new InvestmentPurposesInnovationPage()

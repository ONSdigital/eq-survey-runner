// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class AcquisitionInternalInvestmentRDPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('acquisition-internal-investment-r-d')
  }

  clickAcquisitionInternalInvestmentRDAnswerYes() {
    browser.element('[id="acquisition-internal-investment-r-d-answer-0"]').click()
    return this
  }

  clickAcquisitionInternalInvestmentRDAnswerNo() {
    browser.element('[id="acquisition-internal-investment-r-d-answer-1"]').click()
    return this
  }

}

export default new AcquisitionInternalInvestmentRDPage()

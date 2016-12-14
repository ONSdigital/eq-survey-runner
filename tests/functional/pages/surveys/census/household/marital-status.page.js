// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.764533 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MaritalStatusPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('marital-status')
  }

  clickMaritalStatusAnswerNeverMarriedAndNeverRegisteredASameSexCivilPartnership() {
    browser.element('[id="marital-status-answer-1"]').click()
    return this
  }

  clickMaritalStatusAnswerMarried() {
    browser.element('[id="marital-status-answer-2"]').click()
    return this
  }

  clickMaritalStatusAnswerInARegisteredSameSexCivilPartnership() {
    browser.element('[id="marital-status-answer-3"]').click()
    return this
  }

  clickMaritalStatusAnswerSeparatedButStillLegallyMarried() {
    browser.element('[id="marital-status-answer-4"]').click()
    return this
  }

  clickMaritalStatusAnswerSeparatedButStillLegallyInASameSexCivilPartnership() {
    browser.element('[id="marital-status-answer-5"]').click()
    return this
  }

  clickMaritalStatusAnswerDivorced() {
    browser.element('[id="marital-status-answer-6"]').click()
    return this
  }

  clickMaritalStatusAnswerFormerlyInASameSexCivilPartnershipWhichIsNowLegallyDissolved() {
    browser.element('[id="marital-status-answer-7"]').click()
    return this
  }

  clickMaritalStatusAnswerWidowed() {
    browser.element('[id="marital-status-answer-8"]').click()
    return this
  }

  clickMaritalStatusAnswerSurvivingPartnerFromASameSexCivilPartnership() {
    browser.element('[id="marital-status-answer-9"]').click()
    return this
  }

}

export default new MaritalStatusPage()

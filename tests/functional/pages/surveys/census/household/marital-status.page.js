import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MaritalStatusPage extends MultipleChoiceWithOtherPage {

  clickNeverMarriedAndNeverRegisteredASameSexCivilPartnership() {
    browser.element('[id="marital-status-answer-1"]').click()
    return this
  }

  clickMarried() {
    browser.element('[id="marital-status-answer-2"]').click()
    return this
  }

  clickInARegisteredSameSexCivilPartnership() {
    browser.element('[id="marital-status-answer-3"]').click()
    return this
  }

  clickSeparatedButStillLegallyMarried() {
    browser.element('[id="marital-status-answer-4"]').click()
    return this
  }

  clickSeparatedButStillLegallyInASameSexCivilPartnership() {
    browser.element('[id="marital-status-answer-5"]').click()
    return this
  }

  clickDivorced() {
    browser.element('[id="marital-status-answer-6"]').click()
    return this
  }

  clickFormerlyInASameSexCivilPartnershipWhichIsNowLegallyDissolved() {
    browser.element('[id="marital-status-answer-7"]').click()
    return this
  }

  clickWidowed() {
    browser.element('[id="marital-status-answer-8"]').click()
    return this
  }

  clickSurvivingPartnerFromASameSexCivilPartnership() {
    browser.element('[id="marital-status-answer-9"]').click()
    return this
  }

  setMaritalStatusAnswer(value) {
    browser.setValue('[name="marital-status-answer"]', value)
    return this
  }

  getMaritalStatusAnswer(value) {
    return browser.element('[name="marital-status-answer"]').getValue()
  }

}

export default new MaritalStatusPage()

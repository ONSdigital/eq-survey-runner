// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class NationalIdentityPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('national-identity')
  }

  clickNationalIdentityEnglandAnswerEnglish() {
    browser.element('[id="national-identity-england-answer-0"]').click()
    return this
  }

  clickNationalIdentityEnglandAnswerWelsh() {
    browser.element('[id="national-identity-england-answer-1"]').click()
    return this
  }

  clickNationalIdentityEnglandAnswerScottish() {
    browser.element('[id="national-identity-england-answer-2"]').click()
    return this
  }

  clickNationalIdentityEnglandAnswerNorthernIrish() {
    browser.element('[id="national-identity-england-answer-3"]').click()
    return this
  }

  clickNationalIdentityEnglandAnswerBritish() {
    browser.element('[id="national-identity-england-answer-4"]').click()
    return this
  }

  clickNationalIdentityEnglandAnswerOther() {
    browser.element('[id="national-identity-england-answer-5"]').click()
    return this
  }

  setNationalIdentityEnglandAnswerOtherText(value) {
    browser.setValue('[id="national-identity-england-answer-other"]', value)
    return this
  }

  clickNationalIdentityWalesAnswerWelsh() {
    browser.element('[id="national-identity-wales-answer-0"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerEnglish() {
    browser.element('[id="national-identity-wales-answer-1"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerScottish() {
    browser.element('[id="national-identity-wales-answer-2"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerNorthernIrish() {
    browser.element('[id="national-identity-wales-answer-3"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerBritish() {
    browser.element('[id="national-identity-wales-answer-4"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerOther() {
    browser.element('[id="national-identity-wales-answer-5"]').click()
    return this
  }

  setNationalIdentityWalesAnswerOtherText(value) {
    browser.setValue('[id="national-identity-wales-answer-other"]', value)
    return this
  }

}

export default new NationalIdentityPage()

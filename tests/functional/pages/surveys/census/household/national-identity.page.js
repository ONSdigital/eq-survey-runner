// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.786669 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class NationalIdentityPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('national-identity')
  }

  clickNationalIdentityEnglandAnswerEnglish() {
    browser.element('[id="national-identity-england-answer-1"]').click()
    return this
  }

  clickNationalIdentityEnglandAnswerWelsh() {
    browser.element('[id="national-identity-england-answer-2"]').click()
    return this
  }

  clickNationalIdentityEnglandAnswerScottish() {
    browser.element('[id="national-identity-england-answer-3"]').click()
    return this
  }

  clickNationalIdentityEnglandAnswerNorthernIrish() {
    browser.element('[id="national-identity-england-answer-4"]').click()
    return this
  }

  clickNationalIdentityEnglandAnswerBritish() {
    browser.element('[id="national-identity-england-answer-5"]').click()
    return this
  }

  clickNationalIdentityEnglandAnswerOther() {
    browser.element('[id="national-identity-england-answer-6"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerWelsh() {
    browser.element('[id="national-identity-wales-answer-1"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerEnglish() {
    browser.element('[id="national-identity-wales-answer-2"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerScottish() {
    browser.element('[id="national-identity-wales-answer-3"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerNorthernIrish() {
    browser.element('[id="national-identity-wales-answer-4"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerBritish() {
    browser.element('[id="national-identity-wales-answer-5"]').click()
    return this
  }

  clickNationalIdentityWalesAnswerOther() {
    browser.element('[id="national-identity-wales-answer-6"]').click()
    return this
  }

}

export default new NationalIdentityPage()

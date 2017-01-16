// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class SexualIdentityPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('sexual-identity')
  }

  clickSexualIdentityAnswerHeterosexualOrStraight() {
    browser.element('[id="sexual-identity-answer-0"]').click()
    return this
  }

  clickSexualIdentityAnswerGayOrLesbian() {
    browser.element('[id="sexual-identity-answer-1"]').click()
    return this
  }

  clickSexualIdentityAnswerBisexual() {
    browser.element('[id="sexual-identity-answer-2"]').click()
    return this
  }

  clickSexualIdentityAnswerOther() {
    browser.element('[id="sexual-identity-answer-3"]').click()
    return this
  }

  setSexualIdentityAnswerOther(value) {
    browser.setValue('[name="sexual-identity-answer-other"]', value)
    return this
  }

  getSexualIdentityAnswerOther(value) {
    return browser.element('[name="sexual-identity-answer-other"]').getValue()
  }

}

export default new SexualIdentityPage()

import QuestionPage from '../../question.page'

class SexualIdentityPage extends QuestionPage {

  clickHeterosexualOrStraight() {
    browser.element('[id="sexual-identity-answer-1"]').click()
    return this
  }

  clickGayOrLesbian() {
    browser.element('[id="sexual-identity-answer-2"]').click()
    return this
  }

  clickBisexual() {
    browser.element('[id="sexual-identity-answer-3"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="sexual-identity-answer-4"]').click()
    return this
  }

  setSexualIdentityAnswer(value) {
    browser.setValue('[name="sexual-identity-answer"]', value)
    return this
  }

  getSexualIdentityAnswer(value) {
    return browser.element('[name="sexual-identity-answer"]').getValue()
  }

}

export default new SexualIdentityPage()

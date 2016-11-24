import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class SexualIdentityPage extends MultipleChoiceWithOtherPage {

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

}

export default new SexualIdentityPage()

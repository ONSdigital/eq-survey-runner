import QuestionPage from './question.page'

class MultipleChoiceWithOtherPage extends QuestionPage {

  clickOther() {
    browser.element('[data-qa="has-other-option"]').click()
    return this
  }

  otherInputFieldExists() {
    return browser.isExisting('[data-qa="other-option"]')
  }

  isOtherInputFieldVisible() {
    return browser.isVisible('[data-qa="other-option"]')
  }

  setOtherInputField(value) {
    browser.setValue('[data-qa="other-option"]', value)
    return this
  }

  getOtherInputField() {
    return browser.element('[data-qa="other-option"]').getValue()
  }

  clickTopPrevious() {
    browser.element('a[id="top-previous"]').click()
    return this
  }
}

export default MultipleChoiceWithOtherPage

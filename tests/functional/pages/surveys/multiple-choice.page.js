import QuestionPage from './question.page'

class MultipleChoiceWithOtherPage extends QuestionPage {

  clickOther() {
    browser.element('[data-qa="has-other-option"]').click()
    return this
  }

  clickBacon() {
    browser.element('[name="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c"]').click()
    return this
  }

  clickCheese() {
    browser.element('[name="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c"]').click()
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

  clickTopprevious() {
    browser.element('a[id="top-previous"]').click()
    return this
  }
}

export default MultipleChoiceWithOtherPage

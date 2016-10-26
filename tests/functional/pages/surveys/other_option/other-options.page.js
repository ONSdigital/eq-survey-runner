import QuestionPage from '../question.page'

class OtherOptionsPage extends QuestionPage {

  clickOther(){
    browser.element('[data-qa="has-other-option"]').click()
    return this
  }

  otherTextFieldExits() {
    return browser.isExisting('[data-qa="other-option"]')
  }

  errorExists(){
    return browser.isExisting('.js-inpagelink')
  }

  setTextInOtherField(value) {
    browser.setValue('[data-qa="other-option"]', value)
    return this
  }

}

export default new OtherOptionsPage()

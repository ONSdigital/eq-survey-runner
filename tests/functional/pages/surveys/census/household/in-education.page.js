import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class InEducationPage extends MultipleChoiceWithOtherPage {

  clickYes() {
    browser.element('[id="in-education-answer-1"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="in-education-answer-2"]').click()
    return this
  }

  setInEducationAnswer(value) {
    browser.setValue('[name="in-education-answer"]', value)
    return this
  }

  getInEducationAnswer(value) {
    return browser.element('[name="in-education-answer"]').getValue()
  }

}

export default new InEducationPage()

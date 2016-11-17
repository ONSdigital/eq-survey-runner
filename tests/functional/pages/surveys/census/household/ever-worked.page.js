import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EverWorkedPage extends MultipleChoiceWithOtherPage {

  clickYes() {
    browser.element('[id="ever-worked-answer-1"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="ever-worked-answer-2"]').click()
    return this
  }

  setEverWorkedAnswer(value) {
    browser.setValue('[name="ever-worked-answer"]', value)
    return this
  }

  getEverWorkedAnswer(value) {
    return browser.element('[name="ever-worked-answer"]').getValue()
  }

}

export default new EverWorkedPage()

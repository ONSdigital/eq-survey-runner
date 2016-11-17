import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class Over16Page extends MultipleChoiceWithOtherPage {

  clickYes() {
    browser.element('[id="over-16-answer-1"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="over-16-answer-2"]').click()
    return this
  }

  setOver16Answer(value) {
    browser.setValue('[name="over-16-answer"]', value)
    return this
  }

  getOver16Answer(value) {
    return browser.element('[name="over-16-answer"]').getValue()
  }

}

export default new Over16Page()

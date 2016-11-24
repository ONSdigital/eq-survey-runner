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

}

export default new Over16Page()

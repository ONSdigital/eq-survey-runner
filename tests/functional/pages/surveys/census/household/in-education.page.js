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

}

export default new InEducationPage()

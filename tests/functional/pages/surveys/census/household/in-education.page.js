import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class InEducationPage extends MultipleChoiceWithOtherPage {

  clickInEducationAnswerYes() {
    browser.element('[id="in-education-answer-1"]').click()
    return this
  }

  clickInEducationAnswerNo() {
    browser.element('[id="in-education-answer-2"]').click()
    return this
  }

}

export default new InEducationPage()

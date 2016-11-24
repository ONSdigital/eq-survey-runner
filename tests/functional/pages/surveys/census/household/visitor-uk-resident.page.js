import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class VisitorUkResidentPage extends MultipleChoiceWithOtherPage {

  clickVisitorUkResidentAnswerYes() {
    browser.element('[id="visitor-uk-resident-answer-1"]').click()
    return this
  }

  clickVisitorUkResidentAnswerOther() {
    browser.element('[id="visitor-uk-resident-answer-2"]').click()
    return this
  }

}

export default new VisitorUkResidentPage()

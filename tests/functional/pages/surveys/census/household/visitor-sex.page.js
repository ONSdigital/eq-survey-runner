import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class VisitorSexPage extends MultipleChoiceWithOtherPage {

  clickMale() {
    browser.element('[id="visitor-sex-answer-1"]').click()
    return this
  }

  clickFemale() {
    browser.element('[id="visitor-sex-answer-2"]').click()
    return this
  }

}

export default new VisitorSexPage()

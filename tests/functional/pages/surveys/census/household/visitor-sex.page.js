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

  setVisitorSexAnswer(value) {
    browser.setValue('[name="visitor-sex-answer"]', value)
    return this
  }

  getVisitorSexAnswer(value) {
    return browser.element('[name="visitor-sex-answer"]').getValue()
  }

}

export default new VisitorSexPage()

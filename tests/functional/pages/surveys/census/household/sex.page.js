import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class SexPage extends MultipleChoiceWithOtherPage {

  clickMale() {
    browser.element('[id="sex-answer-1"]').click()
    return this
  }

  clickFemale() {
    browser.element('[id="sex-answer-2"]').click()
    return this
  }

}

export default new SexPage()

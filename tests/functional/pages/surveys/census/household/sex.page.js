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

  setSexAnswer(value) {
    browser.setValue('[name="sex-answer"]', value)
    return this
  }

  getSexAnswer(value) {
    return browser.element('[name="sex-answer"]').getValue()
  }

}

export default new SexPage()

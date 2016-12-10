import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PassportsPage extends MultipleChoiceWithOtherPage {

  clickPassportsAnswerUnitedKingdom() {
    browser.element('[id="passports-answer-1"]').click()
    return this
  }

  clickPassportsAnswerIrish() {
    browser.element('[id="passports-answer-2"]').click()
    return this
  }

  clickPassportsAnswerOther() {
    browser.element('[id="passports-answer-3"]').click()
    return this
  }

  clickPassportsAnswerNone() {
    browser.element('[id="passports-answer-4"]').click()
    return this
  }

}

export default new PassportsPage()

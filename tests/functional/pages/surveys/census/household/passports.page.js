import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PassportsPage extends MultipleChoiceWithOtherPage {

  clickUnitedKingdom() {
    browser.element('[id="passports-answer-1"]').click()
    return this
  }

  clickIrish() {
    browser.element('[id="passports-answer-2"]').click()
    return this
  }

  clickNone() {
    browser.element('[id="passports-answer-3"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="passports-answer-4"]').click()
    return this
  }

}

export default new PassportsPage()

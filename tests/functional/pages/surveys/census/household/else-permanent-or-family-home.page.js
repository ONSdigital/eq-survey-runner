import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class ElsePermanentOrFamilyHomePage extends MultipleChoiceWithOtherPage {

  clickYes() {
    browser.element('[id="else-permanent-or-family-home-answer-1"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="else-permanent-or-family-home-answer-2"]').click()
    return this
  }

  setElsePermanentOrFamilyHomeAnswer(value) {
    browser.setValue('[name="else-permanent-or-family-home-answer"]', value)
    return this
  }

  getElsePermanentOrFamilyHomeAnswer(value) {
    return browser.element('[name="else-permanent-or-family-home-answer"]').getValue()
  }

}

export default new ElsePermanentOrFamilyHomePage()

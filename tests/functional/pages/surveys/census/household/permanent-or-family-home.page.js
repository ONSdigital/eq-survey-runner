import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PermanentOrFamilyHomePage extends MultipleChoiceWithOtherPage {

  clickYes() {
    browser.element('[id="permanent-or-family-home-answer-1"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="permanent-or-family-home-answer-2"]').click()
    return this
  }

}

export default new PermanentOrFamilyHomePage()

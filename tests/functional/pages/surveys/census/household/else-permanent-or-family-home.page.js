import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class ElsePermanentOrFamilyHomePage extends MultipleChoiceWithOtherPage {

  clickElsePermanentOrFamilyHomeAnswerYes() {
    browser.element('[id="else-permanent-or-family-home-answer-1"]').click()
    return this
  }

  clickElsePermanentOrFamilyHomeAnswerNo() {
    browser.element('[id="else-permanent-or-family-home-answer-2"]').click()
    return this
  }

}

export default new ElsePermanentOrFamilyHomePage()

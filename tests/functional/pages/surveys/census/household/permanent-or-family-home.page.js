// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PermanentOrFamilyHomePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('permanent-or-family-home')
  }

  clickPermanentOrFamilyHomeAnswerYes() {
    browser.element('[id="permanent-or-family-home-answer-0"]').click()
    return this
  }

  clickPermanentOrFamilyHomeAnswerNo() {
    browser.element('[id="permanent-or-family-home-answer-1"]').click()
    return this
  }

}

export default new PermanentOrFamilyHomePage()

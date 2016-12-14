// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.721866 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PermanentOrFamilyHomePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('permanent-or-family-home')
  }

  clickPermanentOrFamilyHomeAnswerYes() {
    browser.element('[id="permanent-or-family-home-answer-1"]').click()
    return this
  }

  clickPermanentOrFamilyHomeAnswerNo() {
    browser.element('[id="permanent-or-family-home-answer-2"]').click()
    return this
  }

}

export default new PermanentOrFamilyHomePage()

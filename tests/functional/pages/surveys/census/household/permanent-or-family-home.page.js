// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.820533 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PermanentOrFamilyHomePage extends MultipleChoiceWithOtherPage {

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

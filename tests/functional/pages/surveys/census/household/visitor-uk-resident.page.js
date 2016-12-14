// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.883812 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class VisitorUkResidentPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('visitor-uk-resident')
  }

  clickVisitorUkResidentAnswerYesUsuallyLivesInTheUnitedKingdom() {
    browser.element('[id="visitor-uk-resident-answer-1"]').click()
    return this
  }

  clickVisitorUkResidentAnswerOther() {
    browser.element('[id="visitor-uk-resident-answer-2"]').click()
    return this
  }

}

export default new VisitorUkResidentPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

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

  setVisitorUkResidentAnswerOtherText(value) {
    browser.setValue('[id="visitor-uk-resident-answer-2-other"]', value)
    return this
  }

}

export default new VisitorUkResidentPage()

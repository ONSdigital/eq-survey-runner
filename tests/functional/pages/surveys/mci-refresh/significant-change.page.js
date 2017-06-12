// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class SignificantChangePage extends MultipleChoiceWithOtherPage {
  constructor() {
    super('significant-change')
  }
  clickSignificantChangeEstablishedAnswerYes() {
    browser.element('[id="significant-change-established-answer-0"]').click()
    return this
  }
  SignificantChangeEstablishedAnswerYesIsSelected() {
    return browser.element('[id="significant-change-established-answer-0"]').isSelected()
  }
  clickSignificantChangeEstablishedAnswerNo() {
    browser.element('[id="significant-change-established-answer-1"]').click()
    return this
  }
  SignificantChangeEstablishedAnswerNoIsSelected() {
    return browser.element('[id="significant-change-established-answer-1"]').isSelected()
  }
}

export default new SignificantChangePage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class NotNecessaryPossiblePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('not-necessary-possible')
  }

  clickNotNecessaryPossibleAnswerNoNeedDueToPreviousInnovations() {
    browser.element('[id="not-necessary-possible-answer-0"]').click()
    return this
  }

  clickNotNecessaryPossibleAnswerNoNeedDueToMarketConditions() {
    browser.element('[id="not-necessary-possible-answer-1"]').click()
    return this
  }

  clickNotNecessaryPossibleAnswerTheUkDoesNotHaveABusinessEnvironmentWhichEncouragesCompaniesToInnovate() {
    browser.element('[id="not-necessary-possible-answer-2"]').click()
    return this
  }

  clickNotNecessaryPossibleAnswerOther() {
    browser.element('[id="not-necessary-possible-answer-3"]').click()
    return this
  }

}

export default new NotNecessaryPossiblePage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class IntroduceSignificantlyImprovementPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('introduce-significantly-improvement')
  }

  clickIntroduceSignificantlyImprovementAnswerYes() {
    browser.element('[id="introduce-significantly-improvement-answer-0"]').click()
    return this
  }

  clickIntroduceSignificantlyImprovementAnswerNo() {
    browser.element('[id="introduce-significantly-improvement-answer-1"]').click()
    return this
  }

}

export default new IntroduceSignificantlyImprovementPage()

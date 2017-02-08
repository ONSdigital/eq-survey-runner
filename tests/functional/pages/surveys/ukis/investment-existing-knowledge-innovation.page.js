// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class InvestmentExistingKnowledgeInnovationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('investment-existing-knowledge-innovation')
  }

  clickInvestmentExistingKnowledgeInnovationAnswerYes() {
    browser.element('[id="investment-existing-knowledge-innovation-answer-0"]').click()
    return this
  }

  clickInvestmentExistingKnowledgeInnovationAnswerNo() {
    browser.element('[id="investment-existing-knowledge-innovation-answer-1"]').click()
    return this
  }

}

export default new InvestmentExistingKnowledgeInnovationPage()

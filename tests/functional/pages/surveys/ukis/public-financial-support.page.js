// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class PublicFinancialSupportPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('public-financial-support')
  }

  clickPublicFinancialSupportAuthoritiesAnswerYes() {
    browser.element('[id="public-financial-support-authorities-answer-0"]').click()
    return this
  }

  clickPublicFinancialSupportAuthoritiesAnswerNo() {
    browser.element('[id="public-financial-support-authorities-answer-1"]').click()
    return this
  }

  clickPublicFinancialSupportCentralGovernmentAnswerYes() {
    browser.element('[id="public-financial-support-central-government-answer-0"]').click()
    return this
  }

  clickPublicFinancialSupportCentralGovernmentAnswerNo() {
    browser.element('[id="public-financial-support-central-government-answer-1"]').click()
    return this
  }

  clickPublicFinancialSupportEuAnswerYes() {
    browser.element('[id="public-financial-support-eu-answer-0"]').click()
    return this
  }

  clickPublicFinancialSupportEuAnswerNo() {
    browser.element('[id="public-financial-support-eu-answer-1"]').click()
    return this
  }

}

export default new PublicFinancialSupportPage()

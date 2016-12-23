// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CompletionPreferenceEstablishmentPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('completion-preference-establishment')
  }

  clickCompletionPreferenceEstablishmentAnswerOnline() {
    browser.element('[id="completion-preference-establishment-answer-0"]').click()
    return this
  }

  clickCompletionPreferenceEstablishmentAnswerPaper() {
    browser.element('[id="completion-preference-establishment-answer-1"]').click()
    return this
  }

}

export default new CompletionPreferenceEstablishmentPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-14 14:19:14.080786 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CompletionPreferenceEstablishmentPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('completion-preference-establishment')
  }

  clickCompletionPreferenceEstablishmentAnswerOnline() {
    browser.element('[id="completion-preference-establishment-answer-1"]').click()
    return this
  }

  clickCompletionPreferenceEstablishmentAnswerPaper() {
    browser.element('[id="completion-preference-establishment-answer-2"]').click()
    return this
  }

}

export default new CompletionPreferenceEstablishmentPage()

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CompletionPreferenceIndividualPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('completion-preference-individual')
  }

  clickCompletionPreferenceIndividualAnswerOnline() {
    browser.element('[id="completion-preference-individual-answer-0"]').click()
    return this
  }

  clickCompletionPreferenceIndividualAnswerPaper() {
    browser.element('[id="completion-preference-individual-answer-1"]').click()
    return this
  }

  clickCompletionPreferenceIndividualAnswerNotSure() {
    browser.element('[id="completion-preference-individual-answer-2"]').click()
    return this
  }

}

export default new CompletionPreferenceIndividualPage()

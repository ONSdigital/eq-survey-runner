// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-14 14:19:14.075876 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CompletionPreferenceIndividualPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('completion-preference-individual')
  }

  clickCompletionPreferenceIndividualAnswerOnline() {
    browser.element('[id="completion-preference-individual-answer-1"]').click()
    return this
  }

  clickCompletionPreferenceIndividualAnswerPaper() {
    browser.element('[id="completion-preference-individual-answer-2"]').click()
    return this
  }

  clickCompletionPreferenceIndividualAnswerNotSure() {
    browser.element('[id="completion-preference-individual-answer-3"]').click()
    return this
  }

}

export default new CompletionPreferenceIndividualPage()

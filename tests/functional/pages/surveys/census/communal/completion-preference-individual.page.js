import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CompletionPreferenceIndividualPage extends MultipleChoiceWithOtherPage {

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

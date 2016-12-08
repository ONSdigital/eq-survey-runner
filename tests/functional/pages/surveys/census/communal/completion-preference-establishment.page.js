import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CompletionPreferenceEstablishmentPage extends MultipleChoiceWithOtherPage {

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

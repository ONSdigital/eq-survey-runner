import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class WhyPaperEstablishmentPage extends MultipleChoiceWithOtherPage {

  clickWhyPaperEstablishmentAnswerMoreConvenient() {
    browser.element('[id="why-paper-establishment-answer-1"]').click()
    return this
  }

  clickWhyPaperEstablishmentAnswerDonTTrustInternetOrSecurityConcerns() {
    browser.element('[id="why-paper-establishment-answer-2"]').click()
    return this
  }

  clickWhyPaperEstablishmentAnswerOther() {
    browser.element('[id="why-paper-establishment-answer-3"]').click()
    return this
  }

}

export default new WhyPaperEstablishmentPage()

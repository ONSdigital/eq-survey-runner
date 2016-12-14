// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-14 14:19:14.077588 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class WhyPaperIndividualPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('why-paper-individual')
  }

  clickWhyPaperIndividualAnswerMoreConvenient() {
    browser.element('[id="why-paper-individual-answer-1"]').click()
    return this
  }

  clickWhyPaperIndividualAnswerDonTTrustInternetOrSecurityConcerns() {
    browser.element('[id="why-paper-individual-answer-2"]').click()
    return this
  }

  clickWhyPaperIndividualAnswerNoAccessToInternet() {
    browser.element('[id="why-paper-individual-answer-3"]').click()
    return this
  }

  clickWhyPaperIndividualAnswerUnsureHowToUseAComputer() {
    browser.element('[id="why-paper-individual-answer-4"]').click()
    return this
  }

  clickWhyPaperIndividualAnswerOther() {
    browser.element('[id="why-paper-individual-answer-5"]').click()
    return this
  }

}

export default new WhyPaperIndividualPage()

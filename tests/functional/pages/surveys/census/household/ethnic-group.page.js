import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickEthnicGroupAnswerWhite() {
    browser.element('[id="ethnic-group-answer-1"]').click()
    return this
  }

  clickEthnicGroupAnswerMixedMultipleEthnicGroups() {
    browser.element('[id="ethnic-group-answer-2"]').click()
    return this
  }

  clickEthnicGroupAnswerAsianAsianBritish() {
    browser.element('[id="ethnic-group-answer-3"]').click()
    return this
  }

  clickEthnicGroupAnswerBlackAfricanCaribbeanBlackBritish() {
    browser.element('[id="ethnic-group-answer-4"]').click()
    return this
  }

  clickEthnicGroupAnswerOtherEthnicGroup() {
    browser.element('[id="ethnic-group-answer-5"]').click()
    return this
  }

}

export default new EthnicGroupPage()

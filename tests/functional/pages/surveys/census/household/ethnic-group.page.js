import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickWhite() {
    browser.element('[id="ethnic-group-answer-1"]').click()
    return this
  }

  clickMixedMultipleEthnicGroups() {
    browser.element('[id="ethnic-group-answer-2"]').click()
    return this
  }

  clickAsianAsianBritish() {
    browser.element('[id="ethnic-group-answer-3"]').click()
    return this
  }

  clickBlackAfricanCaribbeanBlackBritish() {
    browser.element('[id="ethnic-group-answer-4"]').click()
    return this
  }

  clickOtherEthnicGroup() {
    browser.element('[id="ethnic-group-answer-5"]').click()
    return this
  }

}

export default new EthnicGroupPage()

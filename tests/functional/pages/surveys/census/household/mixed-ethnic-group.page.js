import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MixedEthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickMixedEthnicGroupAnswerWhiteAndBlackCaribbean() {
    browser.element('[id="mixed-ethnic-group-answer-1"]').click()
    return this
  }

  clickMixedEthnicGroupAnswerWhiteAndBlackAfrican() {
    browser.element('[id="mixed-ethnic-group-answer-2"]').click()
    return this
  }

  clickMixedEthnicGroupAnswerWhiteAndAsian() {
    browser.element('[id="mixed-ethnic-group-answer-3"]').click()
    return this
  }

  clickMixedEthnicGroupAnswerOther() {
    browser.element('[id="mixed-ethnic-group-answer-4"]').click()
    return this
  }

}

export default new MixedEthnicGroupPage()

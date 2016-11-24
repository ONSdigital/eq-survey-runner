import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class OtherEthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickOtherEthnicGroupAnswerArab() {
    browser.element('[id="other-ethnic-group-answer-1"]').click()
    return this
  }

  clickOtherEthnicGroupAnswerOther() {
    browser.element('[id="other-ethnic-group-answer-2"]').click()
    return this
  }

}

export default new OtherEthnicGroupPage()

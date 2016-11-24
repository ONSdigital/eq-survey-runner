import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class OtherEthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickArab() {
    browser.element('[id="other-ethnic-group-answer-1"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="other-ethnic-group-answer-2"]').click()
    return this
  }

}

export default new OtherEthnicGroupPage()

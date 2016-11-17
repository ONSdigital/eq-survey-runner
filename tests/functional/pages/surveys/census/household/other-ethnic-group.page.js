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

  setOtherEthnicGroupAnswer(value) {
    browser.setValue('[name="other-ethnic-group-answer"]', value)
    return this
  }

  getOtherEthnicGroupAnswer(value) {
    return browser.element('[name="other-ethnic-group-answer"]').getValue()
  }

}

export default new OtherEthnicGroupPage()

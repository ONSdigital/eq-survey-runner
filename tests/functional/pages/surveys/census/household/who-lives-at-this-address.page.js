import QuestionPage from '../../question.page'

class WhoLivesAtThisAddressPage extends QuestionPage {

  setWhoLivesAtThisAddressAnswer(value) {
    browser.setValue('[name="who-lives-at-this-address-answer"]', value)
    return this
  }

  getWhoLivesAtThisAddressAnswer(value) {
    return browser.element('[name="who-lives-at-this-address-answer"]').getValue()
  }

}

export default new WhoLivesAtThisAddressPage()

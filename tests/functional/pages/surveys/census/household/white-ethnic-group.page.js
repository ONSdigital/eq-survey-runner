import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class WhiteEthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickEnglishWelshScottishNorthernIrishBritish() {
    browser.element('[id="white-ethnic-group-answer-1"]').click()
    return this
  }

  clickIrish() {
    browser.element('[id="white-ethnic-group-answer-2"]').click()
    return this
  }

  clickGypsyOrIrishTraveller() {
    browser.element('[id="white-ethnic-group-answer-3"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="white-ethnic-group-answer-4"]').click()
    return this
  }

}

export default new WhiteEthnicGroupPage()

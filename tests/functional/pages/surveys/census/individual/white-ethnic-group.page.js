import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class WhiteEthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickWhiteEthnicGroupAnswerEnglishWelshScottishNorthernIrishBritish() {
    browser.element('[id="white-ethnic-group-answer-1"]').click()
    return this
  }

  clickWhiteEthnicGroupAnswerIrish() {
    browser.element('[id="white-ethnic-group-answer-2"]').click()
    return this
  }

  clickWhiteEthnicGroupAnswerGypsyOrIrishTraveller() {
    browser.element('[id="white-ethnic-group-answer-3"]').click()
    return this
  }

  clickWhiteEthnicGroupAnswerOther() {
    browser.element('[id="white-ethnic-group-answer-4"]').click()
    return this
  }

}

export default new WhiteEthnicGroupPage()

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class WhiteEthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickWhiteEthnicGroupEnglandAnswerEnglishWelshScottishNorthernIrishBritish() {
    browser.element('[id="white-ethnic-group-england-answer-1"]').click()
    return this
  }

  clickWhiteEthnicGroupEnglandAnswerIrish() {
    browser.element('[id="white-ethnic-group-england-answer-2"]').click()
    return this
  }

  clickWhiteEthnicGroupEnglandAnswerGypsyOrIrishTraveller() {
    browser.element('[id="white-ethnic-group-england-answer-3"]').click()
    return this
  }

  clickWhiteEthnicGroupEnglandAnswerOther() {
    browser.element('[id="white-ethnic-group-england-answer-4"]').click()
    return this
  }

  clickWhiteEthnicGroupWalesAnswerWelshEnglishScottishNorthernIrishBritish() {
    browser.element('[id="white-ethnic-group-wales-answer-1"]').click()
    return this
  }

  clickWhiteEthnicGroupWalesAnswerIrish() {
    browser.element('[id="white-ethnic-group-wales-answer-2"]').click()
    return this
  }

  clickWhiteEthnicGroupWalesAnswerGypsyOrIrishTraveller() {
    browser.element('[id="white-ethnic-group-wales-answer-3"]').click()
    return this
  }

  clickWhiteEthnicGroupWalesAnswerOther() {
    browser.element('[id="white-ethnic-group-wales-answer-4"]').click()
    return this
  }

}

export default new WhiteEthnicGroupPage()

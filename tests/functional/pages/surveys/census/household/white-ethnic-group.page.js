// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class WhiteEthnicGroupPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('white-ethnic-group')
  }

  clickWhiteEthnicGroupEnglandAnswerEnglishWelshScottishNorthernIrishBritish() {
    browser.element('[id="white-ethnic-group-england-answer-0"]').click()
    return this
  }

  clickWhiteEthnicGroupEnglandAnswerIrish() {
    browser.element('[id="white-ethnic-group-england-answer-1"]').click()
    return this
  }

  clickWhiteEthnicGroupEnglandAnswerGypsyOrIrishTraveller() {
    browser.element('[id="white-ethnic-group-england-answer-2"]').click()
    return this
  }

  clickWhiteEthnicGroupEnglandAnswerOther() {
    browser.element('[id="white-ethnic-group-england-answer-3"]').click()
    return this
  }

  setWhiteEthnicGroupEnglandAnswerOther(value) {
    browser.setValue('[name="white-ethnic-group-england-answer-other"]', value)
    return this
  }

  getWhiteEthnicGroupEnglandAnswerOther(value) {
    return browser.element('[name="white-ethnic-group-england-answer-other"]').getValue()
  }

  clickWhiteEthnicGroupWalesAnswerWelshEnglishScottishNorthernIrishBritish() {
    browser.element('[id="white-ethnic-group-wales-answer-0"]').click()
    return this
  }

  clickWhiteEthnicGroupWalesAnswerIrish() {
    browser.element('[id="white-ethnic-group-wales-answer-1"]').click()
    return this
  }

  clickWhiteEthnicGroupWalesAnswerGypsyOrIrishTraveller() {
    browser.element('[id="white-ethnic-group-wales-answer-2"]').click()
    return this
  }

  clickWhiteEthnicGroupWalesAnswerOther() {
    browser.element('[id="white-ethnic-group-wales-answer-3"]').click()
    return this
  }

  setWhiteEthnicGroupWalesQuestionOther(value) {
    browser.setValue('[name="white-ethnic-group-wales-question-other"]', value)
    return this
  }

  getWhiteEthnicGroupWalesQuestionOther(value) {
    return browser.element('[name="white-ethnic-group-wales-question-other"]').getValue()
  }

}

export default new WhiteEthnicGroupPage()

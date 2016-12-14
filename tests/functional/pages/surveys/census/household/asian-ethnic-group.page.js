// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.799950 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AsianEthnicGroupPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('asian-ethnic-group')
  }

  clickAsianEthnicGroupAnswerIndian() {
    browser.element('[id="asian-ethnic-group-answer-1"]').click()
    return this
  }

  clickAsianEthnicGroupAnswerPakistani() {
    browser.element('[id="asian-ethnic-group-answer-2"]').click()
    return this
  }

  clickAsianEthnicGroupAnswerBangladeshi() {
    browser.element('[id="asian-ethnic-group-answer-3"]').click()
    return this
  }

  clickAsianEthnicGroupAnswerChinese() {
    browser.element('[id="asian-ethnic-group-answer-4"]').click()
    return this
  }

  clickAsianEthnicGroupAnswerOther() {
    browser.element('[id="asian-ethnic-group-answer-5"]').click()
    return this
  }

}

export default new AsianEthnicGroupPage()

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AsianEthnicGroupPage extends MultipleChoiceWithOtherPage {

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

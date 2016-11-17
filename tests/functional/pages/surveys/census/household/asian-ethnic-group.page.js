import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class AsianEthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickIndian() {
    browser.element('[id="asian-ethnic-group-answer-1"]').click()
    return this
  }

  clickPakistani() {
    browser.element('[id="asian-ethnic-group-answer-2"]').click()
    return this
  }

  clickBangladeshi() {
    browser.element('[id="asian-ethnic-group-answer-3"]').click()
    return this
  }

  clickChinese() {
    browser.element('[id="asian-ethnic-group-answer-4"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="asian-ethnic-group-answer-5"]').click()
    return this
  }

  setAsianEthnicGroupAnswer(value) {
    browser.setValue('[name="asian-ethnic-group-answer"]', value)
    return this
  }

  getAsianEthnicGroupAnswer(value) {
    return browser.element('[name="asian-ethnic-group-answer"]').getValue()
  }

}

export default new AsianEthnicGroupPage()

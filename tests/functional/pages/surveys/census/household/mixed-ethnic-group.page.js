import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MixedEthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickWhiteAndBlackCaribbean() {
    browser.element('[id="mixed-ethnic-group-answer-1"]').click()
    return this
  }

  clickWhiteAndBlackAfrican() {
    browser.element('[id="mixed-ethnic-group-answer-2"]').click()
    return this
  }

  clickWhiteAndAsian() {
    browser.element('[id="mixed-ethnic-group-answer-3"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="mixed-ethnic-group-answer-4"]').click()
    return this
  }

  setMixedEthnicGroupAnswer(value) {
    browser.setValue('[name="mixed-ethnic-group-answer"]', value)
    return this
  }

  getMixedEthnicGroupAnswer(value) {
    return browser.element('[name="mixed-ethnic-group-answer"]').getValue()
  }

}

export default new MixedEthnicGroupPage()

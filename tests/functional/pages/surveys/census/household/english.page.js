import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EnglishPage extends MultipleChoiceWithOtherPage {

  clickVeryWell() {
    browser.element('[id="english-answer-1"]').click()
    return this
  }

  clickWell() {
    browser.element('[id="english-answer-2"]').click()
    return this
  }

  clickNotWell() {
    browser.element('[id="english-answer-3"]').click()
    return this
  }

  clickNotAtAll() {
    browser.element('[id="english-answer-4"]').click()
    return this
  }

}

export default new EnglishPage()

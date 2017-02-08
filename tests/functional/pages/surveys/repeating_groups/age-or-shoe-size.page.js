import QuestionPage from '../question.page'

class AgeOrShoeSizePage extends QuestionPage {

  clickAgeAndShoeSize() {
    browser.element('input[id="conditional-answer-0"]').click()
    return this
  }

  clickShoeSizeOnly() {
    browser.element('input[id="conditional-answer-1"]').click()
    return this
  }

}

export default new AgeOrShoeSizePage()

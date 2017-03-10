import QuestionPage from '../question.page'

class TextareaSummaryPage extends QuestionPage {

  constructor() {
    super('textarea-summary')
  }

  getAnswer() {
    return browser.element('[data-qa="answer-answer"]').getText()
  }

}

export default new TextareaSummaryPage()

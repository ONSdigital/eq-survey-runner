import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EverWorkedPage extends MultipleChoiceWithOtherPage {

  clickEverWorkedAnswerYes() {
    browser.element('[id="ever-worked-answer-1"]').click()
    return this
  }

  clickEverWorkedAnswerNo() {
    browser.element('[id="ever-worked-answer-2"]').click()
    return this
  }

}

export default new EverWorkedPage()

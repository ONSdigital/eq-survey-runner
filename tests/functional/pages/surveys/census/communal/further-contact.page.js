import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class FurtherContactPage extends MultipleChoiceWithOtherPage {

  clickFurtherContactAnswerYes() {
    browser.element('[id="further-contact-answer-1"]').click()
    return this
  }

  clickFurtherContactAnswerNo() {
    browser.element('[id="further-contact-answer-2"]').click()
    return this
  }

}

export default new FurtherContactPage()

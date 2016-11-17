import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class DetailsCorrectPage extends MultipleChoiceWithOtherPage {

  clickYesThisIsMyFullName() {
    browser.element('[id="details-correct-answer-1"]').click()
    return this
  }

  clickNoINeedToChangeMyName() {
    browser.element('[id="details-correct-answer-2"]').click()
    return this
  }

  setDetailsCorrectAnswer(value) {
    browser.setValue('[name="details-correct-answer"]', value)
    return this
  }

  getDetailsCorrectAnswer(value) {
    return browser.element('[name="details-correct-answer"]').getValue()
  }

}

export default new DetailsCorrectPage()

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

}

export default new DetailsCorrectPage()

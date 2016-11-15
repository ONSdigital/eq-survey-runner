import QuestionPage from '../question.page'

class NumberOfRepeatsPage extends QuestionPage {

  setNumberOfRepeats(numberOfRepeats) {
    browser.setValue('input[name="no-of-repeats-answer"]', numberOfRepeats)
    return this
  }

}

export default new NumberOfRepeatsPage()

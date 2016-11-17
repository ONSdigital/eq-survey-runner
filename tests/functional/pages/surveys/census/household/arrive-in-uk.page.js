import QuestionPage from '../../question.page'

class ArriveInUkPage extends QuestionPage {

  setArriveInUkAnswer(value) {
    browser.setValue('[name="arrive-in-uk-answer"]', value)
    return this
  }

  getArriveInUkAnswer(value) {
    return browser.element('[name="arrive-in-uk-answer"]').getValue()
  }

}

export default new ArriveInUkPage()

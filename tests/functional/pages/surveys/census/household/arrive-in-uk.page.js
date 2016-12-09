// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.866190 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class ArriveInUkPage extends QuestionPage {

  setArriveInUkAnswerMonth(value) {
    browser.selectByValue('[name="arrive-in-uk-answer-month"]', value)
    return this
  }

  getArriveInUkAnswerMonth(value) {
    return browser.element('[name="arrive-in-uk-answer-month"]').getValue()
  }

  setArriveInUkAnswerYear(value) {
    browser.setValue('[name="arrive-in-uk-answer-year"]', value)
    return this
  }

  getArriveInUkAnswerYear(value) {
    return browser.element('[name="arrive-in-uk-answer-year"]').getValue()
  }

}

export default new ArriveInUkPage()

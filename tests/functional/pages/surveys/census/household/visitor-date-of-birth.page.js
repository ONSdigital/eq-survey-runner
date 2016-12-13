// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.976832 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class VisitorDateOfBirthPage extends QuestionPage {

  setVisitorDateOfBirthAnswerDay(value) {
    browser.setValue('[name="visitor-date-of-birth-answer-day"]', value)
    return this
  }

  getVisitorDateOfBirthAnswerDay(value) {
    return browser.element('[name="visitor-date-of-birth-answer-day"]').getValue()
  }

  setVisitorDateOfBirthAnswerMonth(value) {
    browser.selectByValue('[name="visitor-date-of-birth-answer-month"]', value)
    return this
  }

  getVisitorDateOfBirthAnswerMonth(value) {
    return browser.element('[name="visitor-date-of-birth-answer-month"]').getValue()
  }

  setVisitorDateOfBirthAnswerYear(value) {
    browser.setValue('[name="visitor-date-of-birth-answer-year"]', value)
    return this
  }

  getVisitorDateOfBirthAnswerYear(value) {
    return browser.element('[name="visitor-date-of-birth-answer-year"]').getValue()
  }

}

export default new VisitorDateOfBirthPage()

import QuestionPage from '../../question.page'

class DateOfBirthPage extends QuestionPage {

  setDateOfBirthAnswerDay(value) {
    browser.setValue('[name="date-of-birth-answer-day"]', value)
    return this
  }

  getDateOfBirthAnswerDay(value) {
    return browser.element('[name="date-of-birth-answer-day"]').getValue()
  }

  setDateOfBirthAnswerMonth(value) {
    browser.selectByValue('[name="date-of-birth-answer-month"]', value)
    return this
  }

  getDateOfBirthAnswerMonth(value) {
    return browser.element('[name="date-of-birth-answer-month"]').getValue()
  }

  setDateOfBirthAnswerYear(value) {
    browser.setValue('[name="date-of-birth-answer-year"]', value)
    return this
  }

  getDateOfBirthAnswerYear(value) {
    return browser.element('[name="date-of-birth-answer-year"]').getValue()
  }

}

export default new DateOfBirthPage()

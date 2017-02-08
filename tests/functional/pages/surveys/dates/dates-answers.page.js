import QuestionPage from '../question.page'

class DatesPage extends QuestionPage {

  get dayInput() {
    return browser.element('#input-single-date-answer-day')
  }

  get dayLabel() {
    return browser.element('#label-single-date-answer-day')
  }

  setDateOfBirthDay(day) {
    browser.setValue('[name="single-date-answer-day"]', day)
    return this
  }

  setDateOfBirthMonth(month) {
    browser.selectByValue('[name="single-date-answer-month"]', month)
    return this
  }

  setDateOfBirthYear(year) {
    browser.setValue('[name="single-date-answer-year"]', year)
    return this
  }

  setFromReportingPeriodDay(day) {
    browser.setValue('[name="date-range-from-day"]', day)
    return this
  }

  setFromReportingPeriodMonth(month) {
    browser.selectByValue('[name="date-range-from-month"]', month)
    return this
  }

  setFromReportingPeriodYear(year) {
    browser.setValue('[name="date-range-from-year"]', year)
    return this
  }

  setToReportingPeriodDay(day) {
    browser.setValue('[name="date-range-to-day"]', day)
    return this
  }

  setToReportingPeriodMonth(month) {
    browser.selectByValue('[name="date-range-to-month"]', month)
    return this
  }

  setToReportingPeriodYear(year) {
    browser.setValue('[name="date-range-to-year"]', year)
    return this
  }

  setMonthYearMonth(month) {
    browser.selectByValue('[name="month-year-answer-month"]', month)
    return this
  }

  setMonthYearYear(year) {
    browser.setValue('[name="month-year-answer-year"]', year)
    return this
  }

  setNonMandatoryDateAnswerDay(day) {
    browser.setValue('[name="non-mandatory-date-answer-day"]', day)
    return this
  }

  setNonMandatoryDateAnswerMonth(month) {
    browser.selectByValue('[name="non-mandatory-date-answer-month"]', month)
    return this
  }

  setNonMandatoryDateAnswerYear(year) {
    browser.setValue('[name="non-mandatory-date-answer-year"]', year)
    return this
  }
}

export default new DatesPage()

import QuestionPage from '../question.page'

class MonthlyBusinessSurveyPage extends QuestionPage {

  isOpen() {
    return browser.isExisting('.qa-questionnaire-form')
  }

  setFromReportingPeriodDay(day) {
    browser.setValue('[name="period-from-day"]', day)
    return this
  }

  setFromReportingPeriodMonth(month) {
    browser.selectByValue('[name="period-from-month"]', month)
    return this
  }

  getFromReportingPeriodDay() {
    return browser.element('[name="period-from-day"]');
  }

  setFromReportingPeriodYear(year) {
    browser.setValue('[name="period-from-year"]', year)
    return this
  }

  setToReportingPeriodDay(day) {
    browser.setValue('[name="period-to-day"]', day)
    return this
  }

  setToReportingPeriodMonth(month) {
    browser.selectByValue('[name="period-to-month"]', month)
    return this
  }

  setToReportingPeriodYear(year) {
    browser.setValue('[name="period-to-year"]', year)
    return this
  }

  setRetailBusinessTurnover(amount) {
    browser.setValue('[name="total-retail-turnover"]', amount)
    return this
  }

  focusErrorField() {
    browser.element('.js-inpagelink').click()
  }

}

export default new MonthlyBusinessSurveyPage()

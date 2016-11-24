import QuestionPage from '../question.page'

class MonthlyBusinessSurveyPage extends QuestionPage {

  isOpen() {
    return browser.isExisting('.qa-questionnaire-form')
  }

  setFromReportingPeriodDay(day) {
    browser.setValue('[name="6fd644b0-798e-4a58-a393-a438b32fe637-day"]', day)
    return this
  }

  setFromReportingPeriodMonth(month) {
    browser.selectByValue('[name="6fd644b0-798e-4a58-a393-a438b32fe637-month"]', month)
    return this
  }

  getFromReportingPeriodDay() {
    return browser.element('[name="6fd644b0-798e-4a58-a393-a438b32fe637-day"]');
  }

  setFromReportingPeriodYear(year) {
    browser.setValue('[name="6fd644b0-798e-4a58-a393-a438b32fe637-year"]', year)
    return this
  }

  setToReportingPeriodDay(day) {
    browser.setValue('[name="06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day"]', day)
    return this
  }

  setToReportingPeriodMonth(month) {
    browser.selectByValue('[name="06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month"]', month)
    return this
  }

  setToReportingPeriodYear(year) {
    browser.setValue('[name="06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year"]', year)
    return this
  }

  setRetailBusinessTurnover(amount) {
    browser.setValue('[name="e81adc6d-6fb0-4155-969c-d0d646f15345"]', amount)
    return this
  }

  focusErrorField() {
    browser.element('.js-inpagelink').click()
  }

}

export default new MonthlyBusinessSurveyPage()

class MonthlyBusinessSurveyPage {

  isOpen() {
    return browser.isExisting('.qa-questionnaire-form')
  }

  setFromSalesPeriodDay(day) {
    browser.setValue('[name="6fd644b0-798e-4a58-a393-a438b32fe637-day"]', day)
    return this
  }

  getFromSalesPeriodDay() {
    return browser.element('[name="6fd644b0-798e-4a58-a393-a438b32fe637-day"]');
  }

  setFromSalesPeriodYear(year) {
    browser.setValue('[name="6fd644b0-798e-4a58-a393-a438b32fe637-year"]', year)
    return this
  }

  setToSalesPeriodDay(day) {
    browser.setValue('[name="06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day"]', day)
    return this
  }

  setToSalesPeriodYear(year) {
    browser.setValue('[name="06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year"]', year)
    return this
  }

  setRetailBusinessTurnover(amount) {
    browser.setValue('[name="e81adc6d-6fb0-4155-969c-d0d646f15345"]', amount)
    return this
  }

  focusErrorField() {
    browser.element('.js-inpagelink-trigger').click()
  }

  submit() {
    browser.click('.qa-btn-submit')
    return this
  }

}

export default new MonthlyBusinessSurveyPage()

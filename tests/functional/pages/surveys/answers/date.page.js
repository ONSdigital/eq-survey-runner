class DatePage {
  get dayInput() {
    return browser.element('#input-answer-day')
  }
  get monthInput() {
    return browser.element('#input-answer-month')
  }
  get yearInput() {
    return browser.element('#input-answer-year')
  }
  get dayLabel() {
    return browser.element('#label-answer-day')
  }
  get monthLabel() {
    return browser.element('#label-answer-month')
  }
  get yearLabel() {
    return browser.element('#label-answer-year')
  }
}

export default new DatePage()

import QuestionPage from '../../question.page'

class ReportingPeriodPage extends QuestionPage {

  setFromReportingPeriodDay(day) {
    browser.setValue('[name="94f368e4-7c6c-4272-a780-8c46328626a2-day"]', day)
    return this
  }

  setFromReportingPeriodMonth(month) {
    browser.selectByValue('[name="94f368e4-7c6c-4272-a780-8c46328626a2-month"]', month)
    return this
  }

  setFromReportingPeriodYear(year) {
    browser.setValue('[name="94f368e4-7c6c-4272-a780-8c46328626a2-year"]', year)
    return this
  }

  setToReportingPeriodDay(day) {
    browser.setValue('[name="dc156715-3d48-4af3-afed-7a0a6bb65583-day"]', day)
    return this
  }

  setToReportingPeriodMonth(month) {
    browser.selectByValue('[name="dc156715-3d48-4af3-afed-7a0a6bb65583-month"]', month)
    return this
  }

  setToReportingPeriodYear(year) {
    browser.setValue('[name="dc156715-3d48-4af3-afed-7a0a6bb65583-year"]', year)
    return this
  }

}

export default new ReportingPeriodPage()

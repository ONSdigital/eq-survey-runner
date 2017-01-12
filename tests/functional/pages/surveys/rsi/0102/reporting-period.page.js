import QuestionPage from '../../question.page'

class ReportingPeriodPage extends QuestionPage {

  setFromReportingPeriodDay(day) {
    browser.setValue('[name="period-from-day"]', day)
    return this
  }

  setFromReportingPeriodMonth(month) {
    browser.selectByValue('[name="period-from-month"]', month)
    return this
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

}

export default new ReportingPeriodPage()

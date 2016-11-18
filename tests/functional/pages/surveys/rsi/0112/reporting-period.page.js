import QuestionPage from '../../question.page'

class ReportingPeriodPage extends QuestionPage {

  setFromReportingPeriodDay(day) {
    browser.setValue('[name="fad63234-1083-4f6a-826a-20b5df6e4baa-day"]', day)
    return this
  }

  setFromReportingPeriodMonth(month) {
    browser.selectByValue('[name="fad63234-1083-4f6a-826a-20b5df6e4baa-month"]', month)
    return this
  }

  setFromReportingPeriodYear(year) {
    browser.setValue('[name="fad63234-1083-4f6a-826a-20b5df6e4baa-year"]', year)
    return this
  }

  setToReportingPeriodDay(day) {
    browser.setValue('[name="c8c4bd92-fd45-4fd1-83b6-18c813de2df2-day"]', day)
    return this
  }

  setToReportingPeriodMonth(month) {
    browser.selectByValue('[name="c8c4bd92-fd45-4fd1-83b6-18c813de2df2-month"]', month)
    return this
  }

  setToReportingPeriodYear(year) {
    browser.setValue('[name="c8c4bd92-fd45-4fd1-83b6-18c813de2df2-year"]', year)
    return this
  }

}

export default new ReportingPeriodPage()

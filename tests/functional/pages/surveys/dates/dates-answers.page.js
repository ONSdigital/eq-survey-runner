import QuestionPage from '../question.page'

class DatesPage extends QuestionPage {

  get dayInput() {
    return browser.element('#input-a51b1c7b-3f25-49dd-9275-2ea742eee510-day')
  }

  get dayLabel() {
    return browser.element('#label-a51b1c7b-3f25-49dd-9275-2ea742eee510-day')
  }

  setDateOfBirthDay(day) {
    browser.setValue('[name="a51b1c7b-3f25-49dd-9275-2ea742eee510-day"]', day)
    return this
  }

  setDateOfBirthMonth(month) {
    browser.selectByValue('[name="a51b1c7b-3f25-49dd-9275-2ea742eee510-month"]', month)
    return this
  }

  setDateOfBirthYear(year) {
    browser.setValue('[name="a51b1c7b-3f25-49dd-9275-2ea742eee510-year"]', year)
    return this
  }

  setFromReportingPeriodDay(day) {
    browser.setValue('[name="5b12aea2-ae3b-467d-9291-4d803a444d25-day"]', day)
    return this
  }

  setFromReportingPeriodMonth(month) {
    browser.selectByValue('[name="5b12aea2-ae3b-467d-9291-4d803a444d25-month"]', month)
    return this
  }

  setFromReportingPeriodYear(year) {
    browser.setValue('[name="5b12aea2-ae3b-467d-9291-4d803a444d25-year"]', year)
    return this
  }

  setToReportingPeriodDay(day) {
    browser.setValue('[name="ce42c1f7-a32a-46d5-8183-f54e38616617-day"]', day)
    return this
  }

  setToReportingPeriodMonth(month) {
    browser.selectByValue('[name="ce42c1f7-a32a-46d5-8183-f54e38616617-month"]', month)
    return this
  }

  setToReportingPeriodYear(year) {
    browser.setValue('[name="ce42c1f7-a32a-46d5-8183-f54e38616617-year"]', year)
    return this
  }

  setMonthYearMonth(month) {
    browser.selectByValue('[name="eade17ef-3ec6-46c2-afc7-dffeb07e2e5e-month"]', month)
    return this
  }

  setMonthYearYear(year) {
    browser.setValue('[name="eade17ef-3ec6-46c2-afc7-dffeb07e2e5e-year"]', year)
    return this
  }
}

export default new DatesPage()

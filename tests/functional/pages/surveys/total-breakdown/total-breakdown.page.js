import QuestionPage from '../question.page'

class TotalBreakdownPage extends QuestionPage {

  setPercentage(index, value) {
    browser.setValue('[name="percentage-' + index + '"]', value)
    // Focus on another element so that JS changed event is fired.
    browser.click('[name="total-percentage"]')
    return this
  }

  getTotal() {
    return browser.getValue('[name="total-percentage"]')
  }

  isTotalHighlighted() {
    return browser.getAttribute('[name="total-percentage"]', 'class').indexOf('input--has-error') !== -1
  }

  isTotalReadOnly() {
    return browser.getAttribute('[name="total-percentage"]', 'readonly') === 'true'
  }

}

export default new TotalBreakdownPage()

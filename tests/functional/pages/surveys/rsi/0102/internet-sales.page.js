import QuestionPage from '../../question.page'

class InternetSalesPage extends QuestionPage {

  setInternetSales(sales) {
    browser.setValue('[name="66612bbb-bc06-4d38-b32c-e2a113641c8a"]', sales)
    return this
  }

}

module.exports = new InternetSalesPage()

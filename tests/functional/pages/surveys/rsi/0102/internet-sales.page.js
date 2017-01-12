import QuestionPage from '../../question.page'

class InternetSalesPage extends QuestionPage {

  setInternetSales(sales) {
    browser.setValue('[name="internet-sales-answer"]', sales)
    return this
  }
   getInternetSales() {
    return browser.element('[name="internet-sales-answer"]').getValue()
   }
}

export default new InternetSalesPage()

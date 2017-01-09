import QuestionPage from '../../question.page'

class InternetSalesPage extends QuestionPage {

  setInternetSales(sales) {
    browser.setValue('[name="internet-sales-answer"]', sales)
    return this
  }

}

export default new InternetSalesPage()

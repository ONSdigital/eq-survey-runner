import QuestionPage from '../../question.page'

class InternetSalesPage extends QuestionPage {

  setInternetSales(sales) {
    browser.setValue('[name="78774493-5b64-45c4-8072-22f1a9638095"]', sales)
    return this
  }

}

export default new InternetSalesPage()

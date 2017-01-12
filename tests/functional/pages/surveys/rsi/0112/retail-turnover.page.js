import QuestionPage from '../../question.page'

class RetailTurnoverPage extends QuestionPage {

  setRetailTurnover(turnover) {
    browser.setValue('[name="total-retail-turnover-answer"]', turnover)
    return this
  }

}

export default new RetailTurnoverPage()

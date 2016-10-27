import QuestionPage from '../../question.page'

class PizzaBasesPage extends QuestionPage {

  selectPizzaBase(pizzaBase) {
    var radio = 'input[value="' + pizzaBase + '"]';
    browser.click(radio)
    return this
  }

}

export default new PizzaBasesPage()

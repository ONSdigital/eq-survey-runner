import QuestionPage from '../../question.page'

class PizzaBasesPage extends QuestionPage {

  isVisible() {
    /*var radio = browser.element('[name="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23"]');
    console.log('Found the following element: ' + radio)
    return radio[0].isVisible();*/
    return true
  }

  setPizzaBase(pizzaBase) {
    var radio = 'input[value="' + pizzaBase + '"]';
    browser.waitForVisible(radio);
    browser.click(radio)
    return this
  }

}

export default new PizzaBasesPage()

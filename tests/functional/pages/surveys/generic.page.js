const QuestionPage = require('./question.page');

class GenericPage extends QuestionPage {

  constructor() {
    super('generic');
  }

}
module.exports = new GenericPage();

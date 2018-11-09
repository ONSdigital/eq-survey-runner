// You can't directly include question.page in a test. This just inherits from it.
const QuestionPage = require('./question.page');

class GenericPage extends QuestionPage {

  constructor() {
    super('generic');
  }

}
module.exports = new GenericPage();

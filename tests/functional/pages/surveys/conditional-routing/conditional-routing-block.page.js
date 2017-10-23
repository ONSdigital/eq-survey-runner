// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class ConditionalRoutingBlockPage extends QuestionPage {

  constructor() {
    super('conditional-routing-block');
  }

  yes() {
    return '#conditional-routing-answer-0';
  }

  no() {
    return '#conditional-routing-answer-1';
  }

}
module.exports = new ConditionalRoutingBlockPage();

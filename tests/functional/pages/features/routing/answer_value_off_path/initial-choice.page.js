// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class InitialChoicePage extends QuestionPage {

  constructor() {
    super('initial-choice');
  }

  first() {
    return '#initial-choice-answer-0';
  }

  firstLabel() { return '#label-initial-choice-answer-0'; }

  second() {
    return '#initial-choice-answer-1';
  }

  secondLabel() { return '#label-initial-choice-answer-1'; }

}
module.exports = new InitialChoicePage();

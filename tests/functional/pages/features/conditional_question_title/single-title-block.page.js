// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SingleTitleBlockPage extends QuestionPage {

  constructor() {
    super('single-title-block');
  }

  good() {
    return '#feeling-answer-0';
  }

  goodLabel() { return '#label-feeling-answer-0'; }

  bad() {
    return '#feeling-answer-1';
  }

  badLabel() { return '#label-feeling-answer-1'; }

}
module.exports = new SingleTitleBlockPage();

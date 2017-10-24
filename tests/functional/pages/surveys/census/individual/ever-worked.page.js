// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class EverWorkedPage extends QuestionPage {

  constructor() {
    super('ever-worked');
  }

  yes() {
    return '#ever-worked-answer-0';
  }

  yesLabel() { return '#label-ever-worked-answer-0'; }

  no() {
    return '#ever-worked-answer-1';
  }

  noLabel() { return '#label-ever-worked-answer-1'; }

}
module.exports = new EverWorkedPage();

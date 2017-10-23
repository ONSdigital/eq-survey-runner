// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class InEducationPage extends QuestionPage {

  constructor() {
    super('in-education');
  }

  yes() {
    return '#in-education-answer-0';
  }

  yesLabel() { return '#label-in-education-answer-0'; }

  no() {
    return '#in-education-answer-1';
  }

  noLabel() { return '#label-in-education-answer-1'; }

}
module.exports = new InEducationPage();

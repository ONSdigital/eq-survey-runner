// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class SexPage extends QuestionPage {

  constructor() {
    super('sex');
  }

  male() {
    return '#sex-answer-0';
  }

  maleLabel() { return '#label-sex-answer-0'; }

  female() {
    return '#sex-answer-1';
  }

  femaleLabel() { return '#label-sex-answer-1'; }

}
module.exports = new SexPage();

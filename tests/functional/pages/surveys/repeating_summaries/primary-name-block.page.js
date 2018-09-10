// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../surveys/../question.page');

class PrimaryNameBlockPage extends QuestionPage {

  constructor() {
    super('primary-name-block');
  }

  answer() {
    return '#primary-name';
  }

  answerLabel() { return '#label-primary-name'; }

}
module.exports = new PrimaryNameBlockPage();

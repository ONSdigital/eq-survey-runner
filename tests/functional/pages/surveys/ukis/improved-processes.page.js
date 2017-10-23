// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class ImprovedProcessesPage extends QuestionPage {

  constructor() {
    super('improved-processes');
  }

  yes() {
    return '#improved-processes-answer-0';
  }

  yesLabel() { return '#label-improved-processes-answer-0'; }

  no() {
    return '#improved-processes-answer-1';
  }

  noLabel() { return '#label-improved-processes-answer-1'; }

}
module.exports = new ImprovedProcessesPage();

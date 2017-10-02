// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class ProcessImprovedPage extends QuestionPage {

  constructor() {
    super('process-improved');
  }

  yes() {
    return '#process-improved-answer-0';
  }

  yesLabel() { return '#label-process-improved-answer-0'; }

  no() {
    return '#process-improved-answer-1';
  }

  noLabel() { return '#label-process-improved-answer-1'; }

}
module.exports = new ProcessImprovedPage();

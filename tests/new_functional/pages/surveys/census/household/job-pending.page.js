// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class JobPendingPage extends QuestionPage {

  constructor() {
    super('job-pending');
  }

  yes() {
    return '#job-pending-answer-0';
  }

  no() {
    return '#job-pending-answer-1';
  }

}
module.exports = new JobPendingPage();

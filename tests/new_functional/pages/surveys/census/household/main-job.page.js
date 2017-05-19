// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class MainJobPage extends QuestionPage {

  constructor() {
    super('main-job');
  }

  anEmployee() {
    return '#main-job-answer-0';
  }

  selfEmployedOrFreelanceWithoutEmployees() {
    return '#main-job-answer-1';
  }

  selfEmployedWithEmployees() {
    return '#main-job-answer-2';
  }

}
module.exports = new MainJobPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class JobseekerPage extends QuestionPage {

  constructor() {
    super('jobseeker');
  }

  yes() {
    return '#jobseeker-answer-0';
  }

  no() {
    return '#jobseeker-answer-1';
  }

}
module.exports = new JobseekerPage();

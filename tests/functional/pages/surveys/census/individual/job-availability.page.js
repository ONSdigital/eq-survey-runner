// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class JobAvailabilityPage extends QuestionPage {

  constructor() {
    super('job-availability');
  }

  yes() {
    return '#job-availability-answer-0';
  }

  yesLabel() { return '#label-job-availability-answer-0'; }

  no() {
    return '#job-availability-answer-1';
  }

  noLabel() { return '#label-job-availability-answer-1'; }

}
module.exports = new JobAvailabilityPage();

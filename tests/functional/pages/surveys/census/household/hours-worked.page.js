// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class HoursWorkedPage extends QuestionPage {

  constructor() {
    super('hours-worked');
  }

  answer15OrLess() {
    return '#hours-worked-answer-0';
  }

  answer15OrLessLabel() { return '#label-hours-worked-answer-0'; }

  answer1630() {
    return '#hours-worked-answer-1';
  }

  answer1630Label() { return '#label-hours-worked-answer-1'; }

  answer3148() {
    return '#hours-worked-answer-2';
  }

  answer3148Label() { return '#label-hours-worked-answer-2'; }

  answer49OrMore() {
    return '#hours-worked-answer-3';
  }

  answer49OrMoreLabel() { return '#label-hours-worked-answer-3'; }

}
module.exports = new HoursWorkedPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class VolunteeringPage extends QuestionPage {

  constructor() {
    super('volunteering');
  }

  no() {
    return '#volunteering-answer-0';
  }

  noLabel() { return '#label-volunteering-answer-0'; }

  yesAtLeastOnceAWeek() {
    return '#volunteering-answer-1';
  }

  yesAtLeastOnceAWeekLabel() { return '#label-volunteering-answer-1'; }

  yesLessThanOnceAWeekButAtLeastOnceAMonth() {
    return '#volunteering-answer-2';
  }

  yesLessThanOnceAWeekButAtLeastOnceAMonthLabel() { return '#label-volunteering-answer-2'; }

  yesLessOften() {
    return '#volunteering-answer-3';
  }

  yesLessOftenLabel() { return '#label-volunteering-answer-3'; }

}
module.exports = new VolunteeringPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveDurationPage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-duration');
  }

  durationYears() {
    return '#duration-answer-years';
  }

  durationYearsLabel() {
    return '#label-duration-answer-months';
  }

  durationMonths() {
    return '#duration-answer-months';
  }

  durationMonthsLabel() {
    return '#label-duration-answer-months';
  }

  durationExclusiveIPreferNotToSay() {
    return '#duration-exclusive-answer-0';
  }

  durationExclusiveIPreferNotToSayLabel() { return '#label-duration-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveDurationPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveDatePage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-date');
  }

  dateday() {
    return '#date-answer-day';
  }

  datemonth() {
    return '#date-answer-month';
  }

  dateyear() {
    return '#date-answer-year';
  }

  dateExclusiveIPreferNotToSay() {
    return '#date-exclusive-answer-0';
  }

  dateExclusiveIPreferNotToSayLabel() { return '#label-date-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveDatePage();

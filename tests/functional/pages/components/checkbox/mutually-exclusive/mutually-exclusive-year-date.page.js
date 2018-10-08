// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveYearDatePage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-year-date');
  }

  yearDateYear() {
    return '#year-date-answer-year';
  }

  yearDateYearLabel() {
    return '#label-year-date-answer-year';
  }

  yearDateExclusiveIPreferNotToSay() {
    return '#year-date-exclusive-answer-0';
  }

  yearDateExclusiveIPreferNotToSayLabel() { return '#label-year-date-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveYearDatePage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class LengthOfStayPage extends QuestionPage {

  constructor() {
    super('length-of-stay');
  }

  lessThan6Months() {
    return '#length-of-stay-answer-0';
  }

  answer6MonthsOrMoreButLessThan12Months() {
    return '#length-of-stay-answer-1';
  }

  answer12MonthsOrMore() {
    return '#length-of-stay-answer-2';
  }

}
module.exports = new LengthOfStayPage();

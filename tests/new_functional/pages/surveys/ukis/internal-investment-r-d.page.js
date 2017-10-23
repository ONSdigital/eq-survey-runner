// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class InternalInvestmentRDPage extends QuestionPage {

  constructor() {
    super('internal-investment-r-d');
  }

  yes() {
    return '#internal-investment-r-d-answer-0';
  }

  yesLabel() { return '#label-internal-investment-r-d-answer-0'; }

  no() {
    return '#internal-investment-r-d-answer-1';
  }

  noLabel() { return '#label-internal-investment-r-d-answer-1'; }

}
module.exports = new InternalInvestmentRDPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class FourthNumberBlockPage extends QuestionPage {

  constructor() {
    super('fourth-number-block');
  }

  fourthNumber() {
    return '#fourth-number-answer';
  }

  fourthNumberLabel() { return '#label-fourth-number-answer'; }

  fourthNumberAlsoInTotal() {
    return '#fourth-number-answer-also-in-total';
  }

  fourthNumberAlsoInTotalLabel() { return '#label-fourth-number-answer-also-in-total'; }

}
module.exports = new FourthNumberBlockPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class ThirdNumberBlockPage extends QuestionPage {

  constructor() {
    super('third-number-block');
  }

  thirdNumber() {
    return '#third-number-answer';
  }

  thirdNumberLabel() { return '#label-third-number-answer'; }

  thirdNumberUnitTotal() {
    return '#third-number-answer-unit-total';
  }

  thirdNumberUnitTotalLabel() { return '#label-third-number-answer-unit-total'; }

}
module.exports = new ThirdNumberBlockPage();

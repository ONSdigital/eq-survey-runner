// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SecondNumberBlockPage extends QuestionPage {

  constructor() {
    super('second-number-block');
  }

  secondNumber() {
    return '#second-number-answer';
  }

  secondNumberLabel() { return '#label-second-number-answer'; }

  secondNumberUnitTotal() {
    return '#second-number-answer-unit-total';
  }

  secondNumberUnitTotalLabel() { return '#label-second-number-answer-unit-total'; }

  secondNumberAlsoInTotal() {
    return '#second-number-answer-also-in-total';
  }

  secondNumberAlsoInTotalLabel() { return '#label-second-number-answer-also-in-total'; }

}
module.exports = new SecondNumberBlockPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class RadioNonMandatoryPage extends QuestionPage {

  constructor() {
    super('radio-non-mandatory');
  }

  coffee() {
    return '#radio-non-mandatory-answer-0';
  }

  coffeeLabel() { return '#label-radio-non-mandatory-answer-0'; }

  tea() {
    return '#radio-non-mandatory-answer-1';
  }

  teaLabel() { return '#label-radio-non-mandatory-answer-1'; }

}
module.exports = new RadioNonMandatoryPage();

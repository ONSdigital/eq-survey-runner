// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class RadioMandatoryPage extends QuestionPage {

  constructor() {
    super('radio-mandatory');
  }

  coffee() {
    return '#radio-mandatory-answer-0';
  }

  coffeeLabel() { return '#label-radio-mandatory-answer-0'; }

  tea() {
    return '#radio-mandatory-answer-1';
  }

  teaLabel() { return '#label-radio-mandatory-answer-1'; }

}
module.exports = new RadioMandatoryPage();

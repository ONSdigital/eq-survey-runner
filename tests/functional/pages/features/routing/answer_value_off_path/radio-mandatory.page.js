// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class RadioMandatoryPage extends QuestionPage {

  constructor() {
    super('radio-mandatory');
  }

  first() {
    return '#radio-mandatory-answer-0';
  }

  firstLabel() { return '#label-radio-mandatory-answer-0'; }

  second() {
    return '#radio-mandatory-answer-1';
  }

  secondLabel() { return '#label-radio-mandatory-answer-1'; }

}
module.exports = new RadioMandatoryPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class ExtraCoverItemsRadioPage extends QuestionPage {

  constructor() {
    super('extra-cover-items-radio');
  }

  yes() {
    return '#extra-cover-items-radio-answer-0';
  }

  yesLabel() { return '#label-extra-cover-items-radio-answer-0'; }

  no() {
    return '#extra-cover-items-radio-answer-1';
  }

  noLabel() { return '#label-extra-cover-items-radio-answer-1'; }

}
module.exports = new ExtraCoverItemsRadioPage();

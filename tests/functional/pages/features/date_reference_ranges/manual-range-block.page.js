// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class ManualRangeBlockPage extends QuestionPage {

  constructor() {
    super('manual-range-block');
  }

  yes() {
    return '#manual-range-radio-0';
  }

  yesLabel() { return '#label-manual-range-radio-0'; }

  no() {
    return '#manual-range-radio-1';
  }

  noLabel() { return '#label-manual-range-radio-1'; }

}
module.exports = new ManualRangeBlockPage();

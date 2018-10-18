// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveCheckboxPage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-checkbox');
  }

  checkboxBritish() {
    return '#checkbox-answer-0';
  }

  checkboxBritishLabel() { return '#label-checkbox-answer-0'; }

  checkboxIrish() {
    return '#checkbox-answer-1';
  }

  checkboxIrishLabel() { return '#label-checkbox-answer-1'; }

  checkboxOther() {
    return '#checkbox-answer-2';
  }

  checkboxOtherLabel() { return '#label-checkbox-answer-2'; }

  checkboxOtherText() {
    return '#checkbox-child-other-answer';
  }

  checkboxExclusiveIPreferNotToSay() {
    return '#checkbox-exclusive-answer-0';
  }

  checkboxExclusiveIPreferNotToSayLabel() { return '#label-checkbox-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveCheckboxPage();

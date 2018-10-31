// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SetMinMaxBlockPage extends QuestionPage {

  constructor() {
    super('set-min-max-block');
  }

  setMinimum() {
    return '#set-minimum';
  }

  setMinimumLabel() { return '#label-set-minimum'; }

  setMinimumLabelDescription() { return '#label-set-minimum > .label__description'; }

  setMaximum() {
    return '#set-maximum';
  }

  setMaximumLabel() { return '#label-set-maximum'; }

  setMaximumLabelDescription() { return '#label-set-maximum > .label__description'; }

}
module.exports = new SetMinMaxBlockPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class BlockPage extends QuestionPage {

  constructor() {
    super('block');
  }

  percentage1() {
    return '#percentage-1';
  }

  percentage1Label() { return '#label-percentage-1'; }

  percentage2() {
    return '#percentage-2';
  }

  percentage2Label() { return '#label-percentage-2'; }

  percentage3() {
    return '#percentage-3';
  }

  percentage3Label() { return '#label-percentage-3'; }

  percentage4() {
    return '#percentage-4';
  }

  percentage4Label() { return '#label-percentage-4'; }

  totalPercentage() {
    return '#total-percentage';
  }

  totalPercentageLabel() { return '#label-total-percentage'; }

  highlightedTotal() { return '[class$=input--has-error]'; }

}
module.exports = new BlockPage();

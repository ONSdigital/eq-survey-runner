// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  manualRangeRadio(index = 0) { return '#manual-range-radio-' + index + '-answer'; }

  manualRangeRadioEdit(index = 0) { return '[data-qa="manual-range-radio-' + index + '-edit"]'; }

  dateSeparateRadio(index = 0) { return '#date-separate-radio-' + index + '-answer'; }

  dateSeparateRadioEdit(index = 0) { return '[data-qa="date-separate-radio-' + index + '-edit"]'; }

  dateRangeRadio(index = 0) { return '#date-range-radio-' + index + '-answer'; }

  dateRangeRadioEdit(index = 0) { return '[data-qa="date-range-radio-' + index + '-edit"]'; }

  datesTitle(index = 0) { return '#dates-' + index; }

}
module.exports = new SummaryPage();

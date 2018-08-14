// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  manualRangeRadio() { return '#manual-range-radio-answer'; }

  manualRangeRadioEdit() { return '[data-qa="manual-range-radio-edit"]'; }

  dateSeparateRadio() { return '#date-separate-radio-answer'; }

  dateSeparateRadioEdit() { return '[data-qa="date-separate-radio-edit"]'; }

  dateRangeRadio() { return '#date-range-radio-answer'; }

  dateRangeRadioEdit() { return '[data-qa="date-range-radio-edit"]'; }

  datesTitle() { return '#dates'; }

}
module.exports = new SummaryPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dateRange(index = 0) { return '#date-range-from-' + index + '-answer'; }

  dateRangeEdit(index = 0) { return '[data-qa="date-range-from-' + index + '-edit"]'; }

  datesTitle(index = 0) { return '#dates-' + index; }

}
module.exports = new SummaryPage();

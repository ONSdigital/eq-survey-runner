// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  date(index = 0) { return '#date-' + index + '-answer'; }

  dateEdit(index = 0) { return '[data-qa="date-' + index + '-edit"]'; }

  dateRangeTo(index = 0) { return '#date-range-to-' + index + '-answer'; }

  dateRangeToEdit(index = 0) { return '[data-qa="date-range-to-' + index + '-edit"]'; }

  datesTitle(index = 0) { return '#dates-' + index; }

}
module.exports = new SummaryPage();

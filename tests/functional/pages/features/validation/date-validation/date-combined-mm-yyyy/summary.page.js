// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dateRange() { return '#date-range-from-answer'; }

  dateRangeEdit() { return '[data-qa="date-range-from-edit"]'; }

  datesTitle() { return '#dates'; }

}
module.exports = new SummaryPage();

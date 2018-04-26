// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  date() { return '#date-answer'; }

  dateEdit() { return '[data-qa="date-edit"]'; }

  dateRangeTo() { return '#date-range-to-answer'; }

  dateRangeToEdit() { return '[data-qa="date-range-to-edit"]'; }

  datesTitle() { return '#dates'; }

}
module.exports = new SummaryPage();

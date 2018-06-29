// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  monthYearAnswer() { return '#month-year-answer-answer'; }

  monthYearAnswerEdit() { return '[data-qa="month-year-answer-edit"]'; }

  languageGroupTitle() { return '#language-group'; }

}
module.exports = new SummaryPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  monthYearAnswer(index = 0) { return '#month-year-answer-' + index + '-answer'; }

  monthYearAnswerEdit(index = 0) { return '[data-qa="month-year-answer-' + index + '-edit"]'; }

  languageGroupTitle(index = 0) { return '#language-group-' + index; }

}
module.exports = new SummaryPage();

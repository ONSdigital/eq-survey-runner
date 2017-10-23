// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  answer() {
    return '#first-name-answer-answer';
  }

  otherAnswer() {
    return '#surname-answer-answer';
  }

  editFirstName() {
     return '[data-qa="first-name-answer-edit"]';
  }


}
module.exports = new SummaryPage();


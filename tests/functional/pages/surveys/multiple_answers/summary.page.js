// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  answer(index = 0) {
    return '#first-name-answer-' + index + '-answer';
  }

  otherAnswer(index = 0) {
    return '#surname-answer-' + index + '-answer';
  }

  editFirstName(index = 0) {
     return '[data-qa="first-name-answer-' + index + '-edit"]';
  }


}
module.exports = new SummaryPage();


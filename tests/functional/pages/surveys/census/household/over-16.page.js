// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class Over16Page extends QuestionPage {

  constructor() {
    super('over-16');
  }

  yes() {
    return '#over-16-answer-0';
  }

  no() {
    return '#over-16-answer-1';
  }

}
module.exports = new Over16Page();

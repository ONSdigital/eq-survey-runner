// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class RepeatingBlock1Page extends QuestionPage {

  constructor() {
    super('repeating-block-1');
  }

  answer() {
    return '#what-is-your-age';
  }

  answerLabel() { return '#label-what-is-your-age'; }

  personName() {
    return '[data-qa="block-title"]';
  }

}
module.exports = new RepeatingBlock1Page();

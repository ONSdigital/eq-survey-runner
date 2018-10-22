// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class RepeatingNameBlockPage extends QuestionPage {

  constructor() {
    super('repeating-name-block');
  }

  answer() {
    return '#repeating-name';
  }

  answerLabel() { return '#label-repeating-name'; }

}
module.exports = new RepeatingNameBlockPage();

// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class NumberQuestionPage extends QuestionPage {

  constructor() {
    super('number-question');
  }

  answer() {
    return '#answer';
  }

  answerLabel() { return '#label-answer'; }

}
module.exports = new NumberQuestionPage();

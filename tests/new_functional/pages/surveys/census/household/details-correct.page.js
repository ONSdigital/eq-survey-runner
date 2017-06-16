// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class DetailsCorrectPage extends QuestionPage {

  constructor() {
    super('details-correct');
  }

  yesThisIsMyFullName() {
    return '#details-correct-answer-0';
  }

  noINeedToChangeMyName() {
    return '#details-correct-answer-1';
  }

}
module.exports = new DetailsCorrectPage();

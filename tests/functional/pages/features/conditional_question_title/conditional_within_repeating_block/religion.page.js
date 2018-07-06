// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class ReligionPage extends QuestionPage {

  constructor() {
    super('religion');
  }

  noReligion() {
    return '#religion-answer-0';
  }

  noReligionLabel() { return '#label-religion-answer-0'; }

  jedi() {
    return '#religion-answer-1';
  }

  jediLabel() { return '#label-religion-answer-1'; }

}
module.exports = new ReligionPage();

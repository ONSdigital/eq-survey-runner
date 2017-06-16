// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class CorrectNamePage extends QuestionPage {

  constructor() {
    super('correct-name');
  }

  correctFirstName() {
    return '#correct-first-name';
  }

  correctFirstNameLabel() { return '#label-correct-first-name'; }

  correctMiddleNames() {
    return '#correct-middle-names';
  }

  correctMiddleNamesLabel() { return '#label-correct-middle-names'; }

  correctLastName() {
    return '#correct-last-name';
  }

  correctLastNameLabel() { return '#label-correct-last-name'; }

}
module.exports = new CorrectNamePage();

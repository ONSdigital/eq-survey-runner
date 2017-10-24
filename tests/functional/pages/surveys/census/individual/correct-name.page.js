// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class CorrectNamePage extends QuestionPage {

  constructor() {
    super('correct-name');
  }

  firstName() {
    return '#first-name';
  }

  firstNameLabel() { return '#label-first-name'; }

  middleNames() {
    return '#middle-names';
  }

  middleNamesLabel() { return '#label-middle-names'; }

  lastName() {
    return '#last-name';
  }

  lastNameLabel() { return '#label-last-name'; }

}
module.exports = new CorrectNamePage();

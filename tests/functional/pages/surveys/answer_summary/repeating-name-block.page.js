// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class RepeatingNameBlockPage extends QuestionPage {

  constructor() {
    super('repeating-name-block');
  }

  repeatingFirstName() {
    return '#repeating-first-name';
  }

  repeatingFirstNameLabel() { return '#label-repeating-first-name'; }

  repeatingLastName() {
    return '#repeating-last-name';
  }

  repeatingLastNameLabel() { return '#label-repeating-last-name'; }

}
module.exports = new RepeatingNameBlockPage();

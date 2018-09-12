// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class PrimaryNameBlockPage extends QuestionPage {

  constructor() {
    super('primary-name-block');
  }

  primaryFirstName() {
    return '#primary-first-name';
  }

  primaryFirstNameLabel() { return '#label-primary-first-name'; }

  primaryLastName() {
    return '#primary-last-name';
  }

  primaryLastNameLabel() { return '#label-primary-last-name'; }

}
module.exports = new PrimaryNameBlockPage();

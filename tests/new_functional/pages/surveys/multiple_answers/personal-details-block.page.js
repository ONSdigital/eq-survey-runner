// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class PersonalDetailsBlockPage extends QuestionPage {

  constructor() {
    super('personal-details-block');
  }

  firstName() {
    return '#first-name-answer';
  }

  firstNameLabel() { return '#label-first-name-answer'; }

  surname() {
    return '#surname-answer';
  }

  surnameLabel() { return '#label-surname-answer'; }

}
module.exports = new PersonalDetailsBlockPage();
